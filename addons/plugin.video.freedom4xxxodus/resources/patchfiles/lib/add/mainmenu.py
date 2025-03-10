# freedom4xxxodus patch
"""
    Copyright (C) 2016 ECHO Coder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from scrapers import *
from scrapers import __all__
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2
import os
import urllib
import base64
import kodi
import log_utils

from resources.lib.modules import utils

import client
import requests
import re
import sys
dialog = xbmcgui.Dialog()
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
from resources.lib.modules.freedom import *


url_dispatcher=utils.url_dispatcher
buildDirectory = utils.buildDir

url_dispatcher.unregister('0')
@url_dispatcher.register('0')
def mainMenu():
    info = translatePath(os.path.join(kodi.addonfolder,'resources/files/information.txt'))
    about=ADDONINFO['string']
    # utils.show_info(about['string'])
    # info = "%s\n%s"% (info,utils.getPluginInfo())
    art = translatePath(os.path.join(
        'special://home/addons/script.freexxxodus.artwork/resources/art/', 'main/%s.png'))
    dirlst = []
    c = []
    c += [
        (kodi.giveColor('Welcome to XXX-O-DUS Version %s' % kodi.get_version(), 'blue', True),
             info, 17, 'icon',
             'Original Code by EchoCoderFalse, Updates by @Nemzzy668, Freedom by Twudat', False),
        ('[COLOR cyan]About XXX-O-DUS[/COLOR]', about, 45, 'icon','', True),
        # ('[COLOR cyan]About FREE-XXX-O-DUS Version %s[/COLOR]' % kodi.get_version(), about, 51, 'icon','', True),
        ('[COLOR yellow]View Changelog[/COLOR]', ADDONINFO['changelog'], 17, 'changelog', 'View XXX-O-DUS Changelog.', False),
        ('[COLOR cyan]About the Freedom Patch[/COLOR]', ADDONINFO['freedom'], 917, 'icon', 'About the Freedom Patch.', True),
        # ('[COLOR orange]Check FREE-XXX-O-DUS Health', None, 45, 'icon', 'Versions', True),
        # ('[COLOR magenta]Install CumWithMe ( New Addon )',None,50,'icon','Versions',False),
        ('Search...', None, 29, 'search', 'Search XXX-O-DUS', True),
        ('[COLOR pink]Live Cams', None, 37, 'webcams', 'Live Cams', True),
        ('[COLOR pink]Live Channels', None, 99, 'livexxx', 'Videos', True),
        ('[COLOR pink]Tubes', None, 4, 'tubes', 'Videos', True), \
        # ('[COLOR pink]Scenes',None,36,'scenes','XXX Scenes',True),
        ('[COLOR pink]Movies', None, 43, 'movies', 'XXX Movies', True), \
        # ('[COLOR pink]Films With Sex In',None,48,'sexfilms','Videos',True),
        ('[COLOR pink]Virtual Reality', None, 42,
             'vr', 'XXX Virtual Reality', True),
        ('[COLOR pink]Hentai', None, 39, 'hentai', 'Hentai', True), \
        # ('Vintage',None,270,'vintage','Vintage',True), \
        # ('[COLOR pink]Fetish',None,40,'fetish','Fetish',True),
        ('[COLOR pink]Pictures', None, 35, 'pics', 'Pictures', True),
        ('[COLOR pink]For Gay Men', None, 47, 'gaymen', 'Videos', True), \
        # ('Comics',None,41,'comics','Comics',True),
        ('[COLOR red]Parental Controls', None, 5, 'parental_controls',
            'View/Change Parental Control Settings.', True),
        ('[COLOR red]Your History', None, 20,
            'history', 'View Your History.', True),
        ('[COLOR red]Your Favourites', None, 23,
            'favourites', 'View Your Favourites.', True),
        ('[COLOR red]Your Downloads', None, 27,
            'downloads', 'View Your Downloads.', True),
        ('[COLOR red]Your Settings', None, 19, 'settings', 'View/Change Addon Settings.', False),

        ('Clear The Cache', None, 49, 'icon',
            'Clear the FREE-XXX-O-DUS Cache and Thumnail Cacheto Factory Settings.', False),
         ('RESET XXX-O-DUS', None, 18, 'reset',
             'Reset XXX-O-DUS to Factory Settings.', False),

    ]


    # icondebug=[]
    for i in c:
        icon = art % i[3] #3 is the icon setting in the list
        # icondebug="%s %s\n%s"%(i[0],icon,icondebug)
        fanart = kodi.addonfanart
        dirlst.append({'name': kodi.giveColor(i[0], 'white'), 'url': i[1], 'mode': i[2],
                      'icon': icon, 'fanart': fanart, 'description': i[4], 'folder': i[5]})

    # dialog.ok("DIRLIST",str(dirlst))
    # showText("art",str(icondebug))
    buildDirectory(dirlst, cache=False)


def showText(heading, text):

    try:
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel(heading)
                win.getControl(5).setText(text)
                quit()
                return
            except:
                pass
    except:
        pass
