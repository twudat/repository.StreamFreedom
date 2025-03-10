#############################################################
#################### START ADDON IMPORTS ####################
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six import PY2

import Main
import requests
import pyxbmct.addonwindow as pyxbmct
from resources.libs import updatecheck
dialog = xbmcgui.Dialog()
#############################################################
#################### SET ADDON ID ###########################
_addon_id_ = 'plugin.video.EntertainMe'
_self_ = xbmcaddon.Addon(id=_addon_id_)
updatecheck.checkupdates()
try:
    pastebinurl = 'https://pastebin.com/raw/fDyq0T62'
    link = requests.get(pastebinurl).content
except:
    pass
try:
    Main.MainWindow()
    quit()
except:
    quit()
    dialog.ok("[COLOR red][B]E[COLOR yellow]nterTain Me[/B][/COLOR]",
              "[COLOR red]Add on Failed To Run Contact @Nemzzy668 On Twitter[/COLOR]")
