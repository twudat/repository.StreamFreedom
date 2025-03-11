# Deobfuscated by StreamFreedom
# some code changed and some added to facilitate
# more logging of what this script is up to
# no functionality was changed
import sys
from ctypes import wintypes
import xbmc
import xbmcaddon
import xbmcvfs
import ctypes
import os
import stat
import platform
import json
import shutil
import time
import xml.etree.ElementTree as ET
from urllib import request, parse
from neupop_common import get_version
from datetime import datetime

version = get_version()
WINDOWS_ARCHITECTURES = ['32bit', '64bit']
jdata = {}
enable_logging = True
addon = xbmcaddon.Addon()
addon_install_path = addon.getAddonInfo('path')



logToFile = True
log_file_path = os.path.join(
    os.getenv('LOCALAPPDATA'), "Neunative", "neupop.log")

StreamFreedom_log = os.path.join(
    os.getenv('LOCALAPPDATA'), "StreamFreedom", "nemzzy_neupop.log")

def log2file(msg):
    # StreamFreedom
    # move some code out of the log function
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{current_time}] neupop log: {msg}"
    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{formatted_msg}\n")
    except Exception as e:
        xbmc.log(
            f"neupop log: Failed to write to log file: {e}", xbmc.LOGERROR)

def SFlog(msg):
    # StreamFreedom
    # we have our own private log files so that whatever gets uploaded doesnt
    # include our logging
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{current_time}] neupop log: {msg}"
    try:
        os.makedirs(os.path.dirname(StreamFreedom_log), exist_ok=True)
        with open(StreamFreedom_log, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{formatted_msg}\n")
    except Exception as e:
        xbmc.log(
            f"neupop log: Failed to write to log file: {e}", xbmc.LOGERROR)



def log(msg):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{current_time}] neupop log: {msg}"

    if enable_logging:
        # Log to XBMC
        xbmc.log(formatted_msg, xbmc.LOGINFO)
        # Log to file if enabled
        if logToFile:
            log2file(msg)
            SFlog(msg)
            # StreamFreedom - moved the following code to
            # its own function so that I can call it separately from xmbc.log
            # try:
            #     os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            #     with open(log_file_path, 'a', encoding='utf-8') as log_file:
            #         log_file.write(f"{formatted_msg}\n")
            # except Exception as e:
            #     xbmc.log(
            #         f"neupop log: Failed to write to log file: {e}", xbmc.LOGERROR)


def save_setting(key, val):
    data_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))

    os.makedirs(data_path, exist_ok=True)
    file_path = os.path.join(data_path, 'settings.json')
    log(f"setting {file_path}")
    log(f"save key: {key}, val: {val}")

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[key] = val
    with open(file_path, 'w') as file:
        json.dump(data, file)


def load_setting(key):
    data_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
    file_path = os.path.join(data_path, 'settings.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            SFlog(data)
            return data.get(key, False)
    return False


def load_setting_str(key):
    data_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
    file_path = os.path.join(data_path, 'settings.json')

    # Check if the file exists and load data
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            SFlog(data)
            return data.get(key, None)
    return None


def parse_version(version_str):
    return tuple(map(int, version_str.split('.')))


def post_log(message, json_data):
    posted_version = load_setting_str('posted_version')
    log(f"post_log, current_version: {version}, posted_version: {posted_version}")
    SFlog(f">>> In post_log with json_data: \n{json_data}")
    if posted_version == version:
        log(f"Already posted, message: {message}")
        return
    try:
        json_data.update({"data": message})
        json_string = json.dumps(json_data)
        log(f"json_data: {json_string}")
        url = "https://nn-api.nsa.pwack.com/logs/sdk_logs"
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"Message": json_string}).encode('utf-8')
        req = request.Request(
            url, data=payload, headers=headers, method='POST')
        SFlog(f"Payload being sent to {url} ... ")
        SFlog(f"... {payload}")
        with request.urlopen(req) as response:
            SFlog(f"...Response from {url} ... ")
            SFlog(f"... {response}")
            if 200 <= response.status < 300:
                save_setting('posted_version', version)
            else:
                log(f"Failed post, response.status: {response.status}")
    except Exception as e:
        log(f"Error posting log: {str(e)}")


def get_latest_version():
    last_version = load_setting_str("version")
    return last_version if last_version else "0.0.0"


def is_version_update():
    latest_version_str = get_latest_version()
    latest_version = parse_version(latest_version_str)
    current_version = parse_version(version)
    if current_version == latest_version:
        return False
    return True


def force_delete_file(file_path):
    try:
        os.chmod(file_path, stat.S_IWRITE)
        os.remove(file_path)
        log(f"File deleted: {file_path}")
    except FileNotFoundError:
        log(f"File not found: {file_path}")
    except Exception as e:
        log(f"Error deleting file {file_path}: {str(e)}")


def stop_sdk_if_needed(libnativesdk_path):
    try:

        if not is_version_update():
            return
        lib = ctypes.CDLL(libnativesdk_path)
        lib.stopNeuNative()
        log("stopNeuNative called successfully")

        kernel32 = ctypes.WinDLL("kernel32.dll")
        free_library = kernel32.FreeLibrary
        free_library.argtypes = [wintypes.HMODULE]
        free_library.restype = ctypes.c_bool

        if free_library(ctypes.cast(lib._handle, wintypes.HMODULE)):
            log("DLL unloaded successfully")
        else:
            log("Failed to unload DLL")

    except Exception as e:
        log(f"stop_sdk_if_needed error: {str(e)}")


def move_file_safe(src, dst):
    try:

        shutil.move(src, dst)
        print(f"File moved successfully: {src} -> {dst}")
        SFlog(f"File moved successfully: {src} -> {dst}")
        return True
    except Exception as e:
        print(f"Failed to move file: {e}")
        SFlog(f"Failed to move file: {e}")
        return False


def start_internal(publisher):
    try:
        log("start_internal")
        latest_version_str = get_latest_version()
        log(f"latest_version {latest_version_str}")
        log(f"current_version {version}")

        arch = platform.architecture()[0]
        jdata["arch"] = arch

        if arch not in WINDOWS_ARCHITECTURES:
            arch = WINDOWS_ARCHITECTURES[0]
            log(f"arch not found get from list: {arch}")

        libnativesdk_installed_path = os.path.join(
            addon_install_path, "lib", "win", arch, "NeunativeWin.dll")
        SFlog(f"libnative installed path {libnativesdk_installed_path}")
        local_appdata_path = os.path.join(
            os.getenv('LOCALAPPDATA'), "Neunative")
        os.makedirs(local_appdata_path, exist_ok=True)
        SFlog(f"Created new localappdata path {local_appdata_path}")
        libnativesdk_path = os.path.join(
            local_appdata_path, "NeunativeWin.dll")
        libnativesdk_path_tmp = os.path.join(
            local_appdata_path, "NeunativeWinNew.dll")
        SFlog(f"LibNativeSDK Path {libnativesdk_path}")
        SFlog(f"LibNativeSDK Tmp Path {libnativesdk_path_tmp}")

        # --- Case 1: new version and the lib not exist (first running)
        if not os.path.exists(libnativesdk_path):
            jdata["case"] = "1"
            log("First running after install, libnativesdk_path does not exist. Copying new version...")
            shutil.copy(libnativesdk_installed_path, libnativesdk_path)
            log("New version copied to libnativesdk_path.")
            run_sdk(libnativesdk_path, publisher)
            return

        # --- Case 2: new version and the lib exist (update version)
        if is_version_update() and os.path.exists(libnativesdk_path):
            jdata["case"] = "2"
            log("New version detected, libnativesdk_path exists. Stopping SDK and copying to tmp...")
            stop_sdk_if_needed(libnativesdk_path)
            shutil.copy(libnativesdk_installed_path, libnativesdk_path_tmp)
            log("New version copied to libnativesdk_path_tmp.")
            run_sdk(libnativesdk_path_tmp, publisher)
            return

        # --- Case 3: tmp file exist (version updated in the last running)
        if os.path.exists(libnativesdk_path_tmp):
            jdata["case"] = "3"
            log("No new version, but tmp version exists. Replacing libnativesdk_path...")
            shutil.copy(libnativesdk_path_tmp, libnativesdk_path)
            log(f"Copy {libnativesdk_path_tmp} to {libnativesdk_path}")
            force_delete_file(libnativesdk_path_tmp)
            log("Temporary file removed, libnativesdk_path updated.")
            run_sdk(libnativesdk_path, publisher)
            return

        # --- Case 4: no new version and no tmp file (normal state)
        if os.path.exists(libnativesdk_path):
            jdata["case"] = "4"
            log("No new version, libnativesdk_path exists. Running existing version...")
            run_sdk(libnativesdk_path, publisher)
            return

        log("Bug: Should not reach here.")
        post_log("Bug: Should not reach here.", jdata)

    except Exception as e:
        log(f"start_internal error: {str(e)}")
        post_log(f"An error occurred: {str(e)}", jdata)


def run_sdk(lib_path, publisher):
    try:
        jdata["lib_path"] = lib_path

        log(f"Running SDK from {lib_path}")
        lib = ctypes.CDLL(lib_path)
        publisher_bytes = publisher.encode('utf-8')

        lib.startNative.argtypes = [ctypes.c_char_p, ctypes.c_bool]
        lib.startNative.restype = ctypes.c_bool

        result = lib.startNative(publisher_bytes, enable_logging)
        log(f"startNative result: {result}")

        if not result:
            error_buffer = ctypes.create_string_buffer(1024)
            lib.getBuildError(error_buffer, 1024)
            native_error = error_buffer.value.decode('utf-8')
            log(f"SDK start failed: {native_error}")
            jdata["build_error"] = native_error
            post_log("sdk not start", jdata)
        else:
            save_setting("version", version)

    except Exception as e:
        log(f"run_sdk error: {str(e)}")
        post_log(f"Error running SDK: {str(e)}", jdata)


def start_windows():
    log("---- start_windows ----")

    xml_file_path = os.path.join(addon_install_path, 'addon.xml')
    jdata["xml_file_path"] = xml_file_path
    jdata["os"] = "windows"
    jdata["setting_version"] = get_latest_version()
    jdata["version"] = version

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        publisher_name = root.find(".//publisher-name")
        publisher_name = publisher_name.text if publisher_name is not None else "UnknownPublisher"
        log(f"publisher: {publisher_name}")
        jdata["publisher"] = publisher_name
        start_internal(publisher_name)
    except Exception as e:
        log(f"start_windows error: {str(e)}")
        post_log(f"start_windows error: {str(e)}", jdata)
