# Deobfuscated by StreamFreedom from XXX-O-DUS version="5.00.023"
from builtins import all,exec,len,open,quit,exit
from kodi_six import xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs
from six.moves.urllib.parse import parse_qs,quote_plus,urlparse,parse_qsl
from six import PY2
import sys
import kodi
import re
import urllib
import os
import shutil
import base64
import time
import requests
from resources.lib.modules import downloaderrepo as tools
from resources.lib.modules import extract
from resources.lib.modules import utils
from resources.lib.modules import freedom
from resources.lib.modules import menus
from resources.lib.modules import mainmenu
from resources.lib.modules import parental
from resources.lib.modules import firstStart
from resources.lib.modules import addon_able
translatePath=xbmc.translatePath if PY2 else xbmcvfs.translatePath
parentalCheck=parental.parentalCheck
# StreamFreedom patch
#
# dialog=xbmcgui.Dialog()
# addon_id="plugin.video.xxx-o-dus"
# AddonTitle="[COLOR pink][B]XXX-O-DUS[/B][/COLOR]"
# dialog=xbmcgui.Dialog()
# settingsxml=translatePath(os.path.join("special://home/userdata/addon_data/"+addon_id,"settings.xml"))
# settingsxml_default=translatePath(os.path.join("special://home/addons/"+addon_id,"resources/settings_default.xml"))
# firstrun=translatePath(os.path.join("special://home/userdata/addon_data/"+addon_id,"firstrun.txt"))
# setupfolders=translatePath(os.path.join("special://home/userdata/addon_data/plugin.video.xxx-o-dus/downloads/"))
# REPO=translatePath(os.path.join("special://home/addons","repository.StreamArmy"))
#
#
# if not os.path.exists(REPO):
#     choice=xbmcgui.Dialog().yesno(AddonTitle,"This Add-on requires [COLOR yellow]The StreamArmy Repo[/COLOR] to be installed to work correctly, and get official updates would you like to install it now?",yeslabel="[B][COLOR white]YES[/COLOR][/B]",nolabel="[B][COLOR grey]NO[/COLOR][/B]")
#     if choice==1:
#         path=translatePath(os.path.join("special://home/addons","packages"))
#         if not os.path.exists(path):
#             os.makedirs(path)
#         url="http://streamarmy.co.uk/repo/repository.StreamArmy-15.0.004.zip"
#         dp=xbmcgui.DialogProgress()
#         if PY2:dp.create(AddonTitle,"","","Downloading [COLOR yellow]The StreamArmy Repo[/COLOR]")
#         else:dp.create(AddonTitle,"Downloading [COLOR yellow]The StreamArmy Repo[/COLOR]")
#         lib=os.path.join(path,"repo.zip")
#         try:
#             os.remove(lib)
#         except:
#             pass
#         tools.download(url,lib,dp)
#         addonfolder=translatePath(os.path.join("special://home","addons"))
#         time.sleep(2)
#         if PY2:dp.update(0,"","Installing [COLOR yellow]The StreamArmy Repo[/COLOR] Please Wait","")
#         else:dp.update(0,"Installing [COLOR yellow]The StreamArmy Repo[/COLOR] Please Wait")
#         extract.all(lib,addonfolder,dp)
#         addon_able.set_enabled("repository.StreamArmy")
#         xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
#         xbmc.executebuiltin("XBMC.UpdateAddonRepos()")
#     else:quit()
# def get_pin(url):
#     try:
#         req=urllib2.Request(url)
#         req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36")
#         response=urllib2.urlopen(req,timeout=5)
#         link=response.read()
#         response.close()
#         link=link.replace("\n","").replace("\r","").replace("\t","").replace("<fanart></fanart>","<fanart>x</fanart>").replace("<thumbnail></thumbnail>","<thumbnail>x</thumbnail>").replace("<utube>","<link>https://www.youtube.com/watch?v=").replace("</utube>","</link>")
#         return link
#     except:quit()
# def CheckParent():
#     pin=kodi.get_setting("pin")
#     if pin=="":pin="EXPIRED"
#     if pin=="EXPIRED":
#         kodi.set_setting("pinused","False")
#         dialog.ok(AddonTitle,"[COLOR aqua]Please visit [COLOR pink]https://pinsystem.co.uk[COLOR aqua] to generate an pin code for [COLOR pink]XXX-O-DUS[COLOR aqua] Addon then enter it after clicking ok[/COLOR]")
#         string=""
#         keyboard=xbmc.Keyboard(string,"[COLOR red]Please Enter Pin Generated From Website[/COLOR]")
#         keyboard.doModal()
#         if keyboard.isConfirmed():
#             string=keyboard.getText()
#             if len(string)>1:
#                 term=string.title().replace(" ","")
#                 kodi.set_setting("pin",term)
#                 CheckParent()
#             else:quit()
#         else:
#             quit()
#     if not "EXPIRED" in pin:
#         pinurlcheck=("https://pinsystem.co.uk/service.php?code=%s&plugin=RnVja1lvdSE" % pin)
#         link=requests.get(pinurlcheck).text
#         if len(link)<=5 or "Pin Expired" in link:
#             kodi.set_setting("pin","EXPIRED")
#             CheckParent()
#         else:
#             registerpin=kodi.get_setting("pinused")
#             if registerpin=="False":
#                 try:
#                     requests.get("https://pinsystem.co.uk/checker.php?code=99999&plugin=XXXODUS").content
#                     kodi.set_setting("pinused","True")
#                 except:pass
#             else:pass
#
#

# def main(argv=None):
#     if sys.argv:argv=sys.argv
#     queries=utils.parse_query(sys.argv[2])
#     mode=queries.get("mode",None)
#     utils.url_dispatcher.dispatch(mode,queries)
#     if kodi.get_setting("dev_debug")=="true":utils.url_dispatcher.showmodes()


# if __name__=="__main__":
#     firstStart.run()
#     CheckParent()
#     parentalCheck()
#     sys.exit(main())


def main(argv=None):
    if sys.argv:
        argv = sys.argv
    queries = utils.parse_query(sys.argv[2])
    mode = queries.get('mode', None)
    utils.url_dispatcher.dispatch(mode, queries)
    if kodi.get_setting('dev_debug') == 'true':
        utils.url_dispatcher.showmodes()

if __name__ == '__main__':
    firstStart.run()
    parentalCheck()
    sys.exit(main())
