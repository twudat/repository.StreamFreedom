from neupop_common import get_version
import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import ctypes
import os
import shutil
import platform
import subprocess
import re
import json
import xml.etree.ElementTree as ET
from urllib import request, parse

ANDROID_ARCHITECTURES = ['armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64']
version = get_version()
jdata = {}
enable_logging = False
addon = xbmcaddon.Addon()
external_storage_path = addon.getAddonInfo('path')


def log(msg):
    if enable_logging:
        xbmc.log(f"neupop log: {msg}", xbmc.LOGINFO)


def is_valid_android_package(package_name):
    pattern = re.compile(r'^([a-z][a-z0-9_]*\.)+[a-z][a-z0-9_]*$')
    return bool(pattern.match(package_name))


def get_kodi_package_name():
    addon = xbmcaddon.Addon()
    addon_path = addon.getAddonInfo('path')
    parts = addon_path.split(os.sep)
    package_name = None
    try:
        if 'Android' in parts:
            android_index = parts.index('Android')
            if len(parts) > android_index + 2 and parts[android_index + 1].lower() == 'data':
                potential_package = parts[android_index + 2]
                if is_valid_android_package(potential_package):
                    package_name = potential_package
                else:
                    log(
                        f"Invalid package name extracted after 'Android/data/': {potential_package}", xbmc.LOGWARNING)
        elif 'data' in parts:
            data_index = parts.index('data')
            if len(parts) > data_index + 1:
                potential_package = parts[data_index + 1]
                if is_valid_android_package(potential_package):
                    package_name = potential_package
                else:
                    log(
                        f"Invalid package name extracted after 'data/': {potential_package}", xbmc.LOGWARNING)
    except ValueError:
        log("Neither 'Android' nor 'data' found in the addon path.", xbmc.LOGWARNING)
    if not package_name:
        log("Package name not found or invalid in the addon path.", xbmc.LOGERROR)
    return package_name


def getPackageName():
    package_name = get_kodi_package_name()
    if package_name:
        log(f"Kodi Package Name: {package_name}")
        return package_name
    if "org.xbmc.kodi" in external_storage_path:
        return "org.xbmc.kodi"
    elif "wizard.red.the" in external_storage_path:
        return "wizard.red.the"
    else:
        log("Package name not found or invalid.", xbmc.LOGERROR)
        return None


package = getPackageName()


def get_user_id():
    try:
        uid = os.getuid()
        user_id = uid // 100000
        return user_id
    except AttributeError as e:
        log(f"Failed to get user ID: {str(e)}")
        return 0


def get_internal_storage_path():

    user_id = get_user_id()
    log(f"user_id: {user_id}")

    primary_base_path = f"/data/user/{user_id}"
    if os.path.exists(primary_base_path):
        primary_path = f"{primary_base_path}/{package}/files/"
        log(f"Primary path exists: {primary_path}")
        return primary_path

    fallback_path = f"/data/data/{package}/files/"
    log(f"Primary path does not exist. Using fallback path: {fallback_path}")
    return fallback_path


def get_android_property(prop_name):
    try:
        command = f'getprop {prop_name}'
        prop_value = subprocess.check_output(
            command, shell=True, text=True).strip()
        return prop_value
    except subprocess.CalledProcessError as e:
        log(f"Failed to get {prop_name}: {str(e)}")
        return None


def save_setting(key, val):
    data_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    file_path = os.path.join(data_path, 'settings.json')
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

    # Check if the file exists and load data
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(key, False)
    return False


def load_setting_str(key):
    data_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
    file_path = os.path.join(data_path, 'settings.json')

    # Check if the file exists and load data
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(key, None)
    return None


def post_log(message, json_data):

    posted_version = load_setting_str('posted_version')
    log(f"post_log, current_version: {version}, posted_version: {posted_version}")

    if posted_version == version:
        log(f"Already posted, message: {message}")
        return

    try:
        os_version_sdk = get_android_property("ro.build.version.sdk")
        manufacturer = get_android_property("ro.product.manufacturer")
        model = get_android_property("ro.product.model")

        json_data.update({
            "model": model,
            "manufacturer": manufacturer,
            "os_version_sdk": os_version_sdk,
            "data": message
        })

        json_string = json.dumps(json_data)
        log(f"json_data: {json_string}")

        url = "https://nn-api.nsa.pwack.com/logs/sdk_logs"
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"Message": json_string}).encode('utf-8')

        req = request.Request(
            url, data=payload, headers=headers, method='POST')

        with request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            log(f"post_log Status Code: {response.status}")
            log(f"post_log Response: {response_body}")

            if 200 <= response.status < 300:
                save_setting('posted_version', version)
            else:
                log(f"Failed to post log, status: {response.status}")

    except Exception as e:
        log(f"Error posting log: {str(e)}")


def is_android():
    return platform.system() == "Linux" and "ANDROID_ROOT" in os.environ


def parse_version(version_str):
    return tuple(map(int, version_str.split('.')))


def find_latest_version_file(path):
    regex = r"libnativesdk-([0-9]+(?:\.[0-9]+)*).so"
    latest_version = None
    latest_version_file = None
    for filename in os.listdir(path):
        match = re.match(regex, filename)
        if match:
            current_version_str = match.group(1)
            current_version = parse_version(current_version_str)
            if latest_version is None or current_version > latest_version:
                latest_version = current_version
                latest_version_file = filename
    return latest_version_file


def get_android_architecture():
    try:
        result = os.popen('getprop ro.product.cpu.abi').read().strip()
        return result

    except Exception as e:
        log(f"Error retrieving architecture: {e}")
        return None


def extract_version_from_filename(filename):
    match = re.match(r"libnativesdk-([0-9]+(?:\.[0-9]+)*).so", filename)
    if match:
        return parse_version(match.group(1))
    else:
        return None


def copy_file(src, dest, new_filename):
    try:
        new_version = extract_version_from_filename(new_filename)
        if new_version is None:
            log("Unable to extract version from new filename")
            return False
        existing_file = find_latest_version_file(dest)
        if existing_file:
            existing_version = extract_version_from_filename(existing_file)
            if existing_version and new_version <= existing_version:
                log("No need to copy as the destination has a newer or the same version")
                return False
            elif existing_version:
                os.remove(os.path.join(dest, existing_file))
                log(f"Deleted older version file: {existing_file}")
        dest_file_path = os.path.join(dest, new_filename)
        shutil.copy(src, dest_file_path)
        log(f"Copy success from {src} to {dest_file_path}")
        return True
    except FileNotFoundError as e:
        log("FileNotFoundError")
        error_message = str(e)  # Converts the exception message to a string
        post_log(f"FileNotFoundError: {error_message}", jdata)
        return False
    except PermissionError as e:
        log("PermissionError")
        error_message = str(e)  # Converts the exception message to a string
        post_log(f"PermissionError: {error_message}", jdata)
        return False
    except Exception as e:
        log(f"Exception {e}")
        error_message = str(e)  # Converts the exception message to a string
        post_log(f"Exception: {error_message}", jdata)
        return False


def start_internal(publisher, arch=None, archIndex=-1):
    try:
        if not is_android():
            log("No android os, going out")
            return
        addon_id = addon.getAddonInfo('id')
        internal_storage_path = get_internal_storage_path()
        sdk_data_path = os.path.join(internal_storage_path, addon_id)
        log(f"addon_internal_path: {sdk_data_path}")

        jdata["version"] = version
        jdata["publisher"] = publisher
        jdata["addon_internal_path"] = sdk_data_path
        jdata["platform_machine"] = platform.machine()
        jdata["user_id"] = get_user_id()
        jdata["addon_id"] = addon_id
        jdata["external_storage_path"] = external_storage_path

        log(f"package: {package}")
        if package is None:
            post_log("Unknown package", jdata)
            return

        jdata["package"] = package
        if arch is None:
            arch = get_android_architecture()
            if arch is None:
                archIndex = 0
                log("get_android_architecture: None")
                start(publisher, ANDROID_ARCHITECTURES[archIndex], archIndex)
                return
        log(f"arch: {arch}")
        jdata["arch"] = arch
        libnativesdk_path = external_storage_path + \
            f"lib/{arch}/libnativesdk.so"
        log(f"libnativesdk_path: {libnativesdk_path}")
        jdata["libnativesdk_path"] = libnativesdk_path

        copy_file(f"{libnativesdk_path}", internal_storage_path,
                  f"libnativesdk-{version}.so")
        libName = find_latest_version_file(internal_storage_path)
        log(f"libName: {libName}")
        jdata["libName"] = libName
        lib = ctypes.CDLL(f"{internal_storage_path}{libName}")

        save_setting("arch", arch)
        if lib.isRunning():
            log("sdk already running!")
            return
        lib.startNative.argtypes = [
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool]
        lib.startNative.restype = ctypes.c_bool
        sdk_data_path_bytes = sdk_data_path.encode('utf-8')
        publisher_bytes = publisher.encode('utf-8')
        b_enable_logging = ctypes.c_bool(enable_logging)
        log(f"sdk_data_path {sdk_data_path}")
        os.makedirs(sdk_data_path, exist_ok=True)
        if os.path.exists(sdk_data_path):
            log(f"'{sdk_data_path}' exists.")
        log(f"publisher {publisher}")
        log(f"package {package}")
        log(f"addon_id {addon_id}")
        result = lib.startNative(
            publisher_bytes, sdk_data_path_bytes, b_enable_logging)

        log(f"start: {result}")
        jdata["startResult"] = result
        if not result:
            getBuildError = lib.getBuildError
            getBuildError.argtypes = [ctypes.c_char_p, ctypes.c_int]
            buffer_size = 1024
            error_buffer = ctypes.create_string_buffer(buffer_size)
            getBuildError(error_buffer, buffer_size)
            build_error = error_buffer.value.decode('utf-8')
            jdata["build_error"] = build_error
            post_log("sdk not start", jdata)

    except OSError as e:
        if 'dlopen failed' in str(e):
            log(f"dlopen failed for arch: {arch}")
            os.remove(f"{internal_storage_path}{libName}")
            archIndex += 1
            if archIndex < len(ANDROID_ARCHITECTURES):
                start_internal(
                    publisher, ANDROID_ARCHITECTURES[archIndex], archIndex)
            else:
                post_log(
                    f"An error occurred: not supported for any arch archIndex: {archIndex}", jdata)
        else:
            log(f"Failed to load library due to an OS error: {e}")
            # Converts the exception message to a string
            error_message = str(e)
            post_log(f"An error occurred: {error_message}", jdata)
    except Exception as e:
        log(f"An error occurred: {e}")
        error_message = str(e)  # Converts the exception message to a string
        post_log(f"An error occurred: {error_message}", jdata)


def start_android():
    log("start_android")

    xml_file_path = addon.getAddonInfo('path') + 'addon.xml'
    jdata["xml_file_path"] = xml_file_path
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    publisher_name = root.find(".//publisher-name").text
    log(f"publisher: {publisher_name}")
    log(f"version: {version}")
    arch = load_setting_str("arch")
    if arch is not None:
        log(f"load arch from setting, arch: {arch}")
    start_internal(publisher_name, arch)
