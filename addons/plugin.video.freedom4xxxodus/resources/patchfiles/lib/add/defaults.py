# freedom4xxxodus patch
from kodi_six import xbmc, xbmcvfs
from six import PY2
import sys,os
from urllib.parse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmc
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath

#Python Programmin style suggests all caps for variables that are to be treated as constants
#since constants dont actually exist in python_version
#we *could, however create a read only class that houses our constants
# check here for a start: https://stackoverflow.com/questions/1735434/class-level-read-only-properties-in-python/1735726#1735726

ADDONINFO={}
ADDONKEYS=[]
GITURL="https://github.com/twudat/free-xxx/raw/main/addons.xml"
ZIPSURL="https://raw.githubusercontent.com/Gujal00/smrzips/master/addons.xml"

GOOD_COLOR="lime"
BAD_COLOR="red"
VER_COLOR = "cyan"
UNKOWN_COLOR = "yellow"
VERSION_NOT_FOUND=999


specific_icon = translatePath(os.path.join(
    'special://home/addons/script.freexxxodus.artwork/resources/art/', '%s/icon.png'))
specific_fanart = translatePath(os.path.join(
    'special://home/addons/script.freexxxodus.artwork/resources/art/', '%s/fanart.jpg'))
