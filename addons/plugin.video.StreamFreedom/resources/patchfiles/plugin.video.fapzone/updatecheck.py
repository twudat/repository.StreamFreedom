# Deobfuscated by StreamFreedom from XXX-O-DUS version="5.00.023"
from kodi_six import xbmc, xbmcaddon, xbmcgui
import sys
import re
import requests
dialog = xbmcgui.Dialog()
AddonTitle = '[COLOR red]FapZone 18+ Only[/COLOR]'
addon_id = 'plugin.video.fapzone'
selfAddon = xbmcaddon.Addon(id=addon_id)


def checkupdates():
    return # StreamFreedom patch
    pin = selfAddon.getSetting('pin')
    if pin == '':
        pin = 'EXPIRED'
    if pin == 'EXPIRED':
        selfAddon.setSetting('pinused', 'False')
        dialog.ok(AddonTitle, "[COLOR pink][B]New Site, NO MORE POP UPS! Please visit [COLOR lime]https://pinsystem.co.uk[COLOR pink] to generate an Access Token For [COLOR lime]FapZone[COLOR pink] then enter it after clicking ok[/B][/COLOR]")
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
                        'https://pinsystem.co.uk/checker.php?code=99999&plugin=FapZone').text
                    selfAddon.setSetting('pinused', 'True')
                except:
                    pass
            else:
                pass
