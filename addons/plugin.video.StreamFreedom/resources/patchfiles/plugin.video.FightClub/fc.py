# Deobfuscated by StreamFreedom from XXX-O-DUS version="5.00.023"
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2
import urllib
import os
import re
import sys
import requests
import resolveurl
import base64
from bs4 import BeautifulSoup
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
addon_id = 'plugin.video.FightClub'
selfAddon = xbmcaddon.Addon(id=addon_id)
AddonTitle = '[COLOR gold][B]F[COLOR silver]ight Club[/B][/COLOR]'
Addonicon = translatePath(os.path.join(
    'special://home/addons/' + addon_id, 'icon.png'))
# addonPath           = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.FightClub')
fanarts = translatePath(os.path.join(
    'special://home/addons/' + addon_id, 'fanart.jpg'))
fanart = translatePath(os.path.join(
    'special://home/addons/' + addon_id, 'fanart.jpg'))
icon = translatePath(os.path.join(
    'special://home/addons/' + addon_id, 'icon.png'))
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def GetMenu():
    GetSubs('https://watchwrestling.ae/')
    # addDir("[COLOR yellow][B]Source One[/B][/COLOR]",'https://wrestlinglive.in/',6,Addonicon,fanarts,'Replays From Source 1')
    # addDir("[COLOR yellow][B]Source Two[/B][/COLOR]",'https://watchwrestlings.in/',6,Addonicon,fanarts,'Replays From Source 2')


def GetSubs(url):
    # addDir('[COLOR orange][B]Latest Added[/B][/COLOR]', 'll', 2, Addonicon, fanart, description='Latest Events Added From Fight Club')
    ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'
    headers = {'User-Agent': ua}
    badresults = ['home', 'more', 'dmca', 'disclaimer']
    link = requests.get(url, headers=headers).text
    soup = BeautifulSoup(link, 'html5lib')
    r = soup.find('ul', id={'menu-primary-menu'})
    for menus in r.find_all('li'):
        title = menus.text
        url2 = menus.a['href']
        if not any(x in title.lower() for x in badresults):
            addDir("[COLOR yellow][B]"+title+"[/B][/COLOR]", url2,
                   3, Addonicon, fanarts, 'Replays From %s' % title)


def GetLatest():
    url = 'https://watchwrestlings.in/'
    ua = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'}
    link = requests.get(url, headers=ua).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('div', class_={'item-img'})
    for i in data:
        try:
            name = i.a['title'].replace('Watch Boxing:', '').replace(
                'Full Show Online Free', '').replace('Watch', '')
            icon = i.img['src']
            url2 = i.a['href']
            addDir("[COLOR yellow][B]"+name+"[/B][/COLOR]",
                   url2, 4, icon, fanarts, '')
        except:
            pass


def CleanWWE(text):
    text = text.replace('Watch', '')
    text = text.replace('Full Show Online Free', '')
    return text


def GetVideos(url):

    ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'
    headers = {'User-Agent': ua}
    link = requests.get(url, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    wrapper = soup.find_all('h2', class_={'entry-title'})
    for i in wrapper:
        name = i.a.text.replace('Watch', '').replace(
            'Full Show Online Free', '').strip()
        url2 = i.a['href']
        addDir("[COLOR yellow][B]"+name+"[/B][/COLOR]", url2,
               4, Addonicon, fanarts, 'Fight Club On Demand')
    try:
        nextpage = soup.find('link', rel={'next'})['href']
        addDir("[COLOR red][B]Next Page --------->[/B][/COLOR]",
               nextpage, 3, Addonicon, fanart)
    except:
        pass


def GetLinks(url, iconimage):
    from random import choice
    IE_USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    OPERA_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97'
    IOS_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1'
    ANDROID_USER_AGENT = 'Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
    EDGE_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
    CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4136.7 Safari/537.36'
    SAFARI_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'

    _USER_AGENTS = [FF_USER_AGENT, OPERA_USER_AGENT,
                    EDGE_USER_AGENT, CHROME_USER_AGENT, SAFARI_USER_AGENT]

    RAND_UA = choice(_USER_AGENTS)
    headers = {'User-Agent': RAND_UA}
    dialog.notification(
        AddonTitle, '[COLOR skyblue]Hunting Playable Links Now, Please Wait[/COLOR]', icon, 5000)
    link = requests.get(url, headers=headers)
    links = 0
    idpattern = r'''href=['"](https://pak-mcqs.*?)['"].+?>(.*?)<'''
    try:
        findid = re.findall(idpattern, link.text, flags=re.DOTALL)
    except:
        dialog.notification(
            AddonTitle, '[COLOR skyblue]Sorry No Playable Links Found, Try Later[/COLOR]', icon, 5000)
        quit()
    for vid, part in findid:
        checklink = requests.get(vid, headers=headers).text
        soup = BeautifulSoup(checklink, 'html.parser')
        source = soup.find('iframe')['src']
        if 'vidsports.xyz' in source:
            try:
                headers = {'User-Agent': RAND_UA,
                           'Referer': vid}
                link2 = requests.get(source, headers=headers).text
                pattern = r'''file:.*?atob\('(.*?)'\)'''
                dl = base64.b64decode(re.findall(pattern, link2)[0])
                dl = dl.decode("utf-8")
                links += 1
                addLink("[COLOR yellow][B]"+part +
                        " Direct Link[/B][/COLOR]", dl, 99, iconimage, fanarts)
            except Exception:
                pass
        else:
            if resolveurl.HostedMediaFile(source).valid_url():
                links += 1
            # title = ('Link %s' % links)
                addLink("[COLOR yellow][B]"+part+" RD LINK[/B][/COLOR]",
                        source, 99, iconimage, fanarts)
            else:
                pass
    if links == 0:
        dialog.notification(
            AddonTitle, '[COLOR skyblue]Sorry No Playable Links Found[/COLOR]', icon, 5000)


def ResolvePakFasion(name, url, iconimage):
    url2 = url.split('|')[0]
    ref = url.split('|')[1]
    ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'
    headers = {'User-Agent': ua,
               'Referer': ref}
    link = requests.get(url2, headers=headers).text
    soup = BeautifulSoup(link, 'html5lib')
    goodmatch = ['primevideo', 'vidlox']
    playable = soup.find('iframe')['src'].replace('\n', '')
    if any(x in playable for x in goodmatch):
        if 'primevideos' in playable:
            try:
                dialog.notification(
                    AddonTitle, '[COLOR skyblue]Prime Link Found[/COLOR]', icon, 2000)
                link2 = requests.get(playable, headers=headers).text
                soup = BeautifulSoup(link2, 'html5lib')
                playable2 = soup.find('iframe')['src'].replace('\n', '')
                headers2 = {'User-Agent': ua,
                            'Referer': playable}
                link3 = requests.get(playable2, headers=headers2).text
                playable = re.findall(
                    '''source:\s+['"](.*?)['"]''', link3, flags=re.DOTALL)[0]
                playable = ('%s|Referer=%s' % (playable, playable2))
                PLAYLINK(name, playable, iconimage)
            except:
                dialog.notification(
                    AddonTitle, '[COLOR skyblue]Couldn\'t Resolve Prime Link[/COLOR]', icon, 5000)
        else:
            PLAYLINK(name, playable, iconimage)
    else:
        dialog.notification(
            AddonTitle, '[COLOR skyblue]No Resolvable Links Available, Sorry![/COLOR]', icon, 5000)


def Open_Link(url):
    UA = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    link = requests.get(url, headers=UA)
    return link.text


def addLink(name, url, mode, iconimage, fanart, description='', family=''):

    u = "%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s&description=%s" % (sys.argv[0], quote_plus(
        url), mode, quote_plus(name), quote_plus(iconimage), quote_plus(fanart), quote_plus(description))
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setArt({"thumb": iconimage})
    liz.setInfo('video', {'Plot': description})
    liz.setProperty('IsPlayable', 'true')
    view = xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    ok = xbmcplugin.addDirectoryItem(handle=int(
        sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addDir(name, url, mode, iconimage, fanart, description=''):
    u = "%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s&description=%s" % (sys.argv[0], quote_plus(
        url), mode, quote_plus(name), quote_plus(iconimage), quote_plus(fanart), quote_plus(description))
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setArt({"thumb": iconimage})
    liz.setInfo('video', {'Plot': description})
    view = xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    ok = xbmcplugin.addDirectoryItem(handle=int(
        sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def PLAYLINK(name, link, iconimage):
    try:
        dialog.notification(
            AddonTitle, '[COLOR yellow]Hunting Link Now Be Patient[/COLOR]', Addonicon, 2500)
        hmf = resolveurl.HostedMediaFile(url=link)
        if hmf.valid_url():
            link = hmf.resolve()
        xbmcplugin.setResolvedUrl(
            int(sys.argv[1]), True, xbmcgui.ListItem(path=link))
        GetMenu()
    except Exception as e:
        dialog.notification(
            AddonTitle, "[B][COLOR yellow]%s[/B][/COLOR]" % str(e), icon, 5000)
        GetMenu()


def checkupdates():
    return # StreamFreedom patch
    pin = selfAddon.getSetting('pin')
    if pin == '':
        pin = 'EXPIRED'
    if pin == 'EXPIRED':
        selfAddon.setSetting('pinused', 'False')
        dialog.ok(AddonTitle, "[COLOR yellow]NEW SITE NO MORE POP UPS! Please visit [COLOR lime]https://pinsystem.co.uk[COLOR yellow] to generate an Access Token For [COLOR lime]FightClub[COLOR yellow] then enter it after clicking ok[/COLOR]")
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
                        'https://pinsystem.co.uk/checker.php?code=99999&plugin=FightClub').text
                    selfAddon.setSetting('pinused', 'True')
                except:
                    pass
            else:
                pass


checkupdates()
params = dict(parse_qsl(sys.argv[2].replace("?", "")))
site = params.get("site", "0")
url = params.get("url", "0")
name = params.get("name", "0")
mode = int(params.get("mode", "0"))
iconimage = params.get("iconimage", "0")
fanart = params.get("fanart", "0")
MovieInfo = description = params.get("description", "0")
if mode == 0 or url == "0" or len(url) < 1:
    GetMenu()
elif mode == 1:
    GetContent(name, url, iconimage, fanart)
elif mode == 2:
    GetLatest()
elif mode == 3:
    GetVideos(url)
elif mode == 4:
    GetLinks(url, iconimage)
elif mode == 5:
    RedditSelect(url)
elif mode == 6:
    GetSubs(url)
elif mode == 41:
    ResolvePakFasion(name, url, iconimage)
elif mode == 99:
    PLAYLINK(name, url, iconimage)
if mode == None or url == None or len(url) < 1:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
else:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
