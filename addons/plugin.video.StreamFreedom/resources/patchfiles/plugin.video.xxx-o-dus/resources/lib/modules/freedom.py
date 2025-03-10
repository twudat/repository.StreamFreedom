# StreamFreedom patch
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2
from six import string_types as six_string_types
if PY2:
    import StringIO
    from xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING
else:
    from io import StringIO
    from kodi_six.xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGINFO as LOGNOTICE, LOGINFO as LOGSEVERE, LOGWARNING

dialog = xbmcgui.Dialog()
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
import sys,urllib,os,base64,re,shutil
import kodi
import client
import dom_parser2
import cache
import log_utils
import pyxbmct
import pprint
import copy
import textwrap
from xml.etree.ElementTree import ElementTree as ET
from resources.lib.modules.defaults import *
from resources.lib.modules import utils
buildDirectory = utils.buildDir
url_dispatcher=utils.url_dispatcher

#Python Programmin style suggests all caps for variables that are to be treated as constants
#since constants dont actually exist in python_version
#we *could, however create a read only class that houses our constants
# check here for a start: https://stackoverflow.com/questions/1735434/class-level-read-only-properties-in-python/1735726#1735726

ADDONINFO=None
ADDONKEYS=[]
GITURL="https://github.com/twudat/free-xxx/raw/main/addons.xml"
ZIPSURL="https://raw.githubusercontent.com/Gujal00/smrzips/master/addons.xml"

GOOD_COLOR="lime"
BAD_COLOR="red"
VER_COLOR = "cyan"
UNKOWN_COLOR = "yellow"
VERSION_NOT_FOUND=999

# changelog_url = 'https://pastebin.com/raw/SgsRvwZV'


specific_icon = translatePath(os.path.join(
    'special://home/addons/script.freexxxodus.artwork/resources/art/', '%s/icon.png'))
specific_fanart = translatePath(os.path.join(
    'special://home/addons/script.freexxxodus.artwork/resources/art/', '%s/fanart.jpg'))

# class Addoninfo:
#     _instance = None
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Addoninfo, cls).__new__(cls)
#             cls._instance.ADDONINFO = None
#         return cls._instance
#

def kodiVersion():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version >= 11.0 and version <= 11.9:
        codename = 'Eden'
    elif version >= 12.0 and version <= 12.9:
        codename = 'Frodo'
    elif version >= 13.0 and version <= 13.9:
        codename = 'Gotham'
    elif version >= 14.0 and version <= 14.9:
        codename = 'Helix'
    elif version >= 15.0 and version <= 15.9:
        codename = 'Isengard'
    elif version >= 16.0 and version <= 16.9:
        codename = 'Jarvis'
    elif version >= 17.0 and version <= 17.9:
        codename = 'Krypton'
    elif version >= 18.0 and version <= 18.9:
        codename = 'Leia'
    elif version >= 19.0 and version <= 19.9:
        codename = 'Matrix'
    elif version >= 20.0 and version <= 20.9:
        codename = 'Nexus'
    elif version >= 21.0 and version <= 21.9:
        codename = 'Omega'
    elif version >= 22.0 and version <= 22.9:
        codename = 'Piers'
    else: codename = "Decline"
    return codename

def unregister(self, mode):
    """
    Funtion to extend url_dispatcher adding an unregister function

    mode: the mode value passed in the plugin:// url

    Useful when replacing a menu function
    """
    mode=mode.strip()
    if mode in self.func_registry:
        value = self.func_registry.pop(mode)
        args = self.args_registry.pop(mode)
        kwargs = self.kwargs_registry.pop(mode)

        line = 'Mode %s unregistered as %s args: %s kwargs: %s' %(str(mode), str(value), str(args), str(kwargs))
        xbmc.log(line, LOGNOTICE)
    else:
        line = 'Mode %s unregistered as %s args: %s kwargs: %s' %(str(mode), str(value), str(args), str(kwargs))
        xbmc.log(line, LOGNOTICE)
        message = 'UrlDispatcher Error: mode %s Is not registered ' % (mode)
        raise Exception(message)
#add our new method to the instance
url_dispatcher.unregister = unregister.__get__(url_dispatcher)

def showmodes(self):
    import xbmc
    for mode in sorted(self.func_registry, key=lambda x: int(x)):
        value = self.func_registry[mode]
        args = self.args_registry[mode]
        kwargs = self.kwargs_registry[mode]
        line = 'Mode %s Registered - %s args: %s kwargs: %s' %(str(mode), str(value), str(args), str(kwargs))
        xbmc.log(line, LOGNOTICE)
url_dispatcher.showmodes = showmodes.__get__(url_dispatcher)
# url_dispatcher.showmodes()
# raise Exception("In Depversions")

def show_info(msg_text="Usage: show_info('Your string of stuff you wanna display')"):
    if isinstance(msg_text, six_string_types):
        items=msg_text.splitlines()
    else:
        items=pprint.pformat(msg_text).splitlines()
    dirlst = []
    for e in items:
        dirlst.append({'name': kodi.giveColor(e,'white'), 'url': e, 'mode': 999, 'icon': 'icon.png', 'fanart': 'fanart.png', 'description': e, 'folder': False})
    buildDirectory(dirlst)


def LoadXml(file):
    """Attempt to load a local or remote
    xml file.
    return the root of the element tree if successful
    return None on fail
    """
    result=None
    success=False
    if ( os.path.exists(file)):
        tree = ET()
        try:
            tree.parse(file)
            success=True
        except:
            pass
    elif file.lower().startswith('http'):
        try:
            file = client.request(file)
            tree = ET.ElementTree(ET.fromstring(file))
            success=True
        except:
            pass
    if success: result = tree.getroot()
    return result


def getPluginInfo(extension=""):#extension='plugin.video.free-xxx-o-dus'):
    """Get everything we know about a plugin or script
       Defaults to this script

       Try to only do this once per session

       Set the global ADDONINFO to None to get it to re-run
    """
    global ADDONINFO
    if not ADDONINFO is None:
        return
    ADDONINFO={}
    splitwidth=45
    key_color='cyan'
    text_color='yellow'
    req_color='white'
    result=ADDONINFO
    rs=""



    for i in ('name','id','version','author','changelog','description','summary','disclaimer','fanart','icon','path','profile'):
        i=i.strip()
        s=xbmcaddon.Addon(extension).getAddonInfo(i)
        s=s.strip()
        if len(s) > 0:
            if len(s) > splitwidth:
                s=s.split('[BR]')
                c=[]
                for sub_s in s:
                    c += textwrap.wrap(sub_s,splitwidth)
                s='\n'.join(c)
            result[i]=s
            i="%s:" % i
            if len(i) <= 8 : adj=16
            else: adj=13
            rs="%s\n%s%s" %(rs,kodi.giveColor(i.ljust(adj),key_color,False),s)


    try: result['xbmc_version']="%s %s" % (kodiVersion(),xbmc.getInfoLabel("System.BuildVersion").split(' ')[0])
    except: result['xbmc_version']='Unknown'
    try: result['xbmc_builddate']=xbmc.getInfoLabel('System.BuildDate')
    except: result['xbmc_builddate']='Unknown'
    try: result['xbmc_language']=xbmc.getInfoLabel('System.Language')
    except: result['xbmc_language']='Unknown'
    try: result['python_version'] = sys.version.split(' ')[0]
    except: result['python_version']='Unknown'

    result['data']=translatePath(os.path.join('special://profile/addon_data/',result['id']))
    result['pattern'] = r'''id=['"]%s['"][\w\s='"-]+version=['"]([^'"]+)['"]''' % result['id']

    localxml = translatePath(os.path.join('special://home/addons/' + result['id'], 'addon.xml'))
    root = LoadXml (localxml)
    p=root.find('requires')
    links = list(p.iter("import"))

    s=[]
    if len(links) > 0:
        rs="%s\n%s :" %(rs,kodi.giveColor('requires','cyan',True))
    for i in links:
        checkdir = translatePath(os.path.join(
                'special://home/addons', i.attrib["addon"]))
        if ( os.path.exists(checkdir)):
            rs="%s\n\t%s" %(rs,kodi.giveColor(i.attrib["addon"],req_color,True))
            s+=[i.attrib["addon"]]

    result['home']=kodi.addonfolder#translatePath(os.path.join('special://home/addons/',result['id']))
    result['data']=translatePath(os.path.join('special://profile/addon_data/',result['id']))
    result['pattern'] = r'''id=['"]%s['"][\w\s='"-]+version=['"]([^'"]+)['"]''' % result['id']
    result['changelog'] = translatePath(os.path.join('special://home/addons/' + result['id'], 'changelog.txt'))
    result['freedom'] = 'The FreeDom Patch is a patch to XXX-O-DUS\nthat sets it free from the pin system and obfuscated code'
    # result['freedom'] = result['changelog']
    result['string'] = "%s\n\n" % rs
    result['requires']=s

    # ADDONINFO=copy.copy(result)
    # raise Exception('getPluginInfo %s' % pprint.pformat(ADDONINFO))
    return

getPluginInfo()

def parse_query(query):
    toint = ['page', 'download', 'favmode', 'channel', 'section']
    q = {'mode': '0'}
    if query.startswith('?'): query = query[1:]
    queries = parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            if key in toint:
                try: q[key] = int(queries[key][0])
                except: q[key] = queries[key][0]
            else:
                q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q


def getChatDBcon(RC=False):
    import sqlite3
    databases = translatePath(os.path.join('special://profile/addon_data/plugin.video.free-xxx-o-dus', 'databases'))
    chaturbatedb = translatePath(os.path.join(databases, 'chaturbate.db'))
    if ( not os.path.exists(databases)):
        os.makedirs(databases)
    conn = sqlite3.connect(chaturbatedb)
    c = conn.cursor()
    try:
        c.executescript("CREATE TABLE IF NOT EXISTS chaturbate (name, url, image);")
    except:
        pass
    if RC == True:
        return conn
    else:
        conn.close()
        return None



def IsOutfDate(Version,Pattern,Haystack):
    global GOOD_COLOR
    global BAD_COLOR
    global UNKOWN_COLOR
    global VERSION_NOT_FOUND

    ver=""
    latest_v=-1
    this_v=-1
    try:
        this_v = int(Version.replace('.',''))
    except:
        pass  #pass these once we know this code aint flakey anymore


    try: # to extract current version from the latest git addon.xml
        ver = re.findall(Pattern, Haystack)[0]
        latest_v = int(ver.replace('.',''))
    except:
        # show_info(re.findall(Pattern, Haystack))
        # show_info((Pattern,Haystack))
        pass
        # dialog.ok("ERRROR",Haystack)
        # raise  #pass these once we know this code aint flakey anymore

    if latest_v < 0:
        return (VERSION_NOT_FOUND,'Version Info Not Found',ver,UNKOWN_COLOR)
    elif this_v < latest_v:
        return (True,'',ver,BAD_COLOR)
    else:
        return (False, "Current",ver,GOOD_COLOR)

@url_dispatcher.register('999')
def DoNothing():
    pass


@utils.url_dispatcher.register('917',['url'])
def FreedomDialog(url):
    if url.startswith('http') or url.startswith('/') :
        viewDialog(url)
    else:
        show_info(url)

url_dispatcher.unregister('17')
@utils.url_dispatcher.register('17',['url'])
def viewDialog(url):
    msg_text=""
    try:
        if url.startswith('http'):
            msg_text = client.request(url)
        else:
            with open(url,mode='r')as f: msg_text = f.read()
    except:
        msg_text="%s - File Not Found!" % url
    from resources.lib.pyxbmct_.github import xxxtext
    #xxxtext.TextWindow(msg_text)
    window = TextBox(Message=msg_text)
    window.doModal()
    del window

url_dispatcher.unregister('45')
@url_dispatcher.register('45')
def depVersions():
    try:
        fxds_xml = client.request(GITURL)
        smrz_xml = client.request(ZIPSURL)
    except:
        kodi.notify(msg='Error opening remote file.', sound = True)
        quit()

    IsOd,IsOd_Message,IsOd_latest,IsOd_Color = IsOutfDate(ADDONINFO['version'],ADDONINFO['pattern'],fxds_xml)

    v_string=kodi.giveColor(ADDONINFO['version'],IsOd_Color,True)
    if IsOd == True: v_string="%s %s You should have %s" % (v_string,
                                    kodi.giveColor(IsOd_Message,IsOd_Color,True),
                                    kodi.giveColor(IsOd_latest,'cyan',True))
    elif IsOd == False: v_string="%s - %s" % (v_string,
                                    kodi.giveColor(IsOd_Message,'white',True))

    c = []

    try:
        c += [(kodi.giveColor('Kodi Version: ','white',True) + kodi.giveColor(ADDONINFO['xbmc_version'],IsOd_Color), ADDONINFO['icon'], ADDONINFO['fanart'], ADDONINFO['xbmc_version'])]
        c += [(kodi.giveColor('Python Version: ','white',True) + kodi.giveColor(ADDONINFO['python_version'],IsOd_Color), ADDONINFO['icon'], ADDONINFO['fanart'], ADDONINFO['python_version'])]
        c += [(kodi.giveColor('Kodi Build Date: ','white',True) + kodi.giveColor(ADDONINFO['xbmc_builddate'],IsOd_Color), ADDONINFO['icon'], ADDONINFO['fanart'], ADDONINFO['xbmc_builddate'])]
        c += [(kodi.giveColor('Kodi Language: ','white',True) + kodi.giveColor(ADDONINFO['xbmc_language'],IsOd_Color), ADDONINFO['icon'], ADDONINFO['fanart'], ADDONINFO['xbmc_language'])]
    except:
        line = 'getPluginInfo %s' % pprint.pformat(ADDONINFO)
        xbmc.log(line, LOGNOTICE)
        raise

    c += [(kodi.giveColor(ADDONINFO['name']+": ",'white',True) + v_string, ADDONINFO['icon'], ADDONINFO['fanart'], ADDONINFO['version'])]
    c += [(kodi.giveColor("Description: ",'white',True) + kodi.giveColor("",'pink'), ADDONINFO['icon'], ADDONINFO['fanart'], "")]

    d = ADDONINFO['description'].split('\n') #textwrap.wrap(ADDONINFO['description'],45)

    for i in d:
        c += [(kodi.giveColor(''.rjust(20,' '),'white',True) + kodi.giveColor(i,'pink'), ADDONINFO['icon'], ADDONINFO['fanart'], i)]


    #Core Modules
    d = []
    # insert a header for core modules
    v_string="%s"% ( kodi.giveColor('~~~~Core Modules~~~~',UNKOWN_COLOR,True))
    d += [(v_string , ADDONINFO['icon'], kodi.addonfanart, 'Core Modules')]

    for i in ADDONINFO['requires']:
        addon_name = xbmcaddon.Addon('%s' % i).getAddonInfo('name')
        addon_id = xbmcaddon.Addon('%s' % i).getAddonInfo('id')
        addon_version = xbmcaddon.Addon('%s' % i).getAddonInfo('version')
        addon_description = xbmcaddon.Addon('%s' % i).getAddonInfo('description')
        addon_icon = xbmcaddon.Addon('%s' % i).getAddonInfo('icon')
        pattern = r'''id=['"]%s['"][\w\s='"-]+version=['"]([^'"]+)['"]''' % addon_id

        IsOd,IsOd_Message,IsOd_latest,IsOd_Color = IsOutfDate(addon_version,pattern,fxds_xml)
        if IsOd == VERSION_NOT_FOUND:
            IsOd,IsOd_Message,IsOd_latest,IsOd_Color = IsOutfDate(addon_version,pattern,smrz_xml)

        v_string=kodi.giveColor(addon_name,'white',True)
        if IsOd == True: v_string="%s %s You should have %s" % (v_string,
                                     kodi.giveColor(IsOd_Message,IsOd_Color,True),
                                     kodi.giveColor(IsOd_latest,'cyan',True))
        elif IsOd == False:
            v_string="%s %s - %s" % (v_string,
                                    kodi.giveColor(addon_version,IsOd_Color ,True),
                                    kodi.giveColor(IsOd_Message,'white',True))


            c += [(v_string , addon_icon, kodi.addonfanart, addon_description)]
        else:
            v_string="%s %s " % (v_string,kodi.giveColor(addon_version,IsOd_Color,True))
            d += [(v_string , addon_icon, kodi.addonfanart, addon_description)]


    dirlst = []
    for e in c:
        dirlst.append({'name': kodi.giveColor(e[0],'white'), 'url': 'None', 'mode': 999, 'icon': e[1], 'fanart': e[2], 'description': e[3], 'folder': False})
    for e in d:
        dirlst.append({'name': kodi.giveColor(e[0],'white'), 'url': 'None', 'mode': 999, 'icon': e[1], 'fanart': e[2], 'description': e[3], 'folder': False})

    # kodi.notify(msg='There you go ..', sound = True)
    buildDirectory(dirlst)

# url_dispatcher.showmodes()

@utils.url_dispatcher.register('49')
def CleanUp():
    Clear_Cache()
    # global msg_text
    msg_text="Cached thumnails have ben purged\n\nOther cache cleaning functions yet to be implemented"
    window = TextBox(Message=msg_text)
    window.doModal()
    del window


def deleteThumbnails():
    thumbnailPath = translatePath('special://thumbnails');
    databasePath = translatePath('special://database')
    msg="Deleted the following Thumnail"
    if os.path.exists(thumbnailPath)==True:
        for root, dirs, files in os.walk(thumbnailPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        msg="\n%s"%os.path.join(root, f)
                        os.unlink(os.path.join(root, f))
                    except:
                        xbmcgui.Dialog().ok("Error", "Unable to remove %s"%os.path.join(root, f))
                    pass

    # xbmcgui.Dialog().ok("Info", msg)

    text13 = os.path.join(databasePath,"Textures13.db")
    if os.path.exists(text13)==True:
        try:
            os.unlink(text13)
        except:
            xbmcgui.Dialog().ok("Error", "Texture13 not removed. %s"% text13)
        pass

def cache_Cleanup():
    try:
        # Resolve the cache path
        cache_path = translatePath("special://cache/")
        xbmc.log(f"[Clear Cache] Resolved cache path: {cache_path}", level=xbmc.LOGDEBUG)

        # Verify path existence
        if not os.path.exists(cache_path):
            xbmcgui.Dialog().ok("Error", "Cache path not found. Operation aborted.")
            xbmc.log(f"[Clear Cache] Cache path not found: {cache_path}", level=xbmc.LOGERROR)
            return

        # Confirm action with the user
        dialog = xbmcgui.Dialog()
        if not dialog.yesno(
            "Clear Cache",
            f"This will delete all files in the cache directory:\n\n{cache_path}\n\nDo you want to continue?",
        ):
            xbmcgui.Dialog().ok("Canceled", "No changes were made.")
            return

        # Delete cache contents
        for item in os.listdir(cache_path):
            item_path = os.path.join(cache_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                xbmc.log(f"[Clear Cache] Deleted: {item_path}", level=xbmc.LOGDEBUG)
            except Exception as e:
                xbmc.log(f"[Clear Cache] Failed to delete {item_path}: {str(e)}", level=xbmc.LOGERROR)

        xbmcgui.Dialog().ok("Success", "Cache has been cleared successfully.")
        xbmc.log("[Clear Cache] Cache cleared successfully.", level=xbmc.LOGINFO)

    except Exception as e:
        xbmcgui.Dialog().ok("Error", f"An error occurred while clearing the cache: {str(e)}")
        xbmc.log(f"[Clear Cache] Critical Error: {str(e)}", level=xbmc.LOGERROR)


def Clear_Cache():
        # cache_Cleanup()
        deleteThumbnails()

class TextBox(pyxbmct.AddonDialogWindow):
    def __init__(self, title='XXX-O-DUS',Message=None,autoscroll=True):
        super(TextBox, self).__init__(title)
        self.setGeometry(950, 600, 10, 30, 0, 5, 5)
        self.set_info_controls(Message,autoscroll)
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self,msg,autoscroll):
        Background   = pyxbmct.Image(translatePath(os.path.join('special://home/addons/script.freexxxodus.artwork', 'resources/art/dialog/bg.jpg')))
        self.placeControl(Background, 0, 0, 10, 30)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 0, 1, 9, 28)
        self.textbox.setText(msg)
        Scroll=autoscroll
        if Scroll:
            self.textbox.autoScroll(1000, 2000, 1000)

        # self.autoscroll=autoscroll

    def set_active_controls(self):
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 9,26,1,4)
        self.connect(self.button, self.close)

    def set_navigation(self):
        self.button.controlUp(self.button)
        self.button.controlDown(self.button)
        self.button.controlRight(self.button)
        self.button.controlLeft(self.button)
        self.setFocus(self.button)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])
