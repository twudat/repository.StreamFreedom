# Deobfuscated by StreamFreedom from XXX-O-DUS version="5.00.023"
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2

import sys
import os
import re
import requests
dialog = xbmcgui.Dialog()
AddonTitle = '[COLOR red][B]E[COLOR yellow]nterTain Me[/B][/COLOR]'
addon_id = 'plugin.video.EntertainMe'
selfAddon = xbmcaddon.Addon(id=addon_id)


def checkupdates():
    return # StreamFreedom patch
    pin = selfAddon.getSetting('pin')
    if pin == '':
        pin = 'EXPIRED'
    if pin == 'EXPIRED':
        selfAddon.setSetting('pinused', 'False')
        dialog.ok(AddonTitle, "[COLOR yellow]New Site, NO MORE POP UPS! Please visit [COLOR lime]https://pinsystem.co.uk[COLOR yellow] to generate an Access Token For [COLOR lime]EntertainMe[COLOR yellow] then enter it after clicking ok[/COLOR]")
        string = ''
        keyboard = xbmc.Keyboard(
            string, '[COLOR red]Please Enter Pin Generated From Website(Case Sensitive)[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            string = keyboard.getText()
            if len(string) > 1:
                term = string.title()
                selfAddon.setSetting('pin', term)
                checkupdates()
            else:
                quit()
        else:
            quit()
    if not 'EXPIRED' in pin:
        pinurlcheck = (
            'https://pinsystem.co.uk/service.php?code=%s&plugin=RnVja1lvdSE' % pin)
        link = requests.get(pinurlcheck).text
        if len(link) <= 2 or 'Pin Expired' in link:
            selfAddon.setSetting('pin', 'EXPIRED')
            checkupdates()
        else:
            registerpin = selfAddon.getSetting('pinused')
            if registerpin == 'False':
                try:
                    requests.get(
                        'https://pinsystem.co.uk/checker.php?code=99999&plugin=EntertainMe').text
                    selfAddon.setSetting('pinused', 'True')
                except:
                    pass
            else:
                pass
