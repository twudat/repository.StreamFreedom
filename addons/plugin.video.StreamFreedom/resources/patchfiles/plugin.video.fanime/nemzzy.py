# Deobfuscated by StreamFreedom
#########################################
############ CODE BY @NEMZZY668###########
#########################################
import jsunpack
import urllib
import os
import re
import sys
import json
import requests
import resolveurl
import random
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2
from bs4 import BeautifulSoup
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
#########################################
addon_id = 'plugin.video.fanime'
selfAddon = xbmcaddon.Addon(id=addon_id)
AddonTitle = '[COLOR magenta][B]FANime[/COLOR][/B]'
Addonfanart = translatePath(os.path.join(
    'special://home/addons/' + addon_id, 'fanart.jpg'))
Addonicon = translatePath(os.path.join(
    'special://home/addons/' + addon_id, 'icon.png'))
AddonDesc = '[COLOR magenta][B]FANime Was Created By @Nemzzy668 ( Follow On Twitter )[/COLOR][/B]'
dialog = xbmcgui.Dialog()
#########################################
user_agent_list = [
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
     "Chrome/77.0.3865.90 Safari/537.36"),
    ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
     "Chrome/79.0.3945.130 Safari/537.36"),
]


def get_headers():
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(user_agent_list),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Sec-Ch-Ua": "Microsoft Edge;v=131, Chromium;v=131, Not_A Brand;v=24",
        "Referer": "https://watch.hikaritv.xyz/"
    }
    return headers


def GetMenu():
    addDir('[COLOR pink][B]Search[/COLOR][/B]', 'null',
           9, Addonicon, Addonfanart, AddonDesc)
    addDir('[COLOR magenta][B]Anime Movies[/COLOR][/B]',
           'https://watch.hikaritv.xyz/type/movies?page=1', 2, Addonicon, Addonfanart, AddonDesc)
    addDir('[COLOR magenta][B]Anime Shows[/COLOR][/B]',
           'https://watch.hikaritv.xyz/type/ona?page=1', 3, Addonicon, Addonfanart, AddonDesc)
    addDir('[COLOR magenta][B]Latest Content[/COLOR][/B]',
           'https://watch.hikaritv.xyz/recently-updated', 2, Addonicon, Addonfanart, AddonDesc)
    addDir('[COLOR magenta][B]Show Genres[/COLOR][/B]',
           'https://watch.hikaritv.xyz/filter?type=1', 5, Addonicon, Addonfanart, AddonDesc)
    addDir('[COLOR magenta][B]Movie Genres[/COLOR][/B]',
           'https://watch.hikaritv.xyz/filter?type=2', 5, Addonicon, Addonfanart, AddonDesc)


def Genres(url):
    link = requests.get(url, headers=get_headers()).text
    soup = BeautifulSoup(link, "html.parser")
    data = soup.find_all('div', class_={'btn'})
    ident = url.split('type=')[1]
    for i in data:
        title = i.text
        url2 = (
            'https://watch.hikaritv.xyz/ajax/getfilter?type=%s&genres=%s&page=1' % (ident, title))
        if str(ident) == '1':
            addDir('[COLOR magenta][B]%s[/COLOR][/B]' %
                   title, url2, 3, Addonicon, Addonfanart, description='')
        else:
            addDir('[COLOR magenta][B]%s[/COLOR][/B]' %
                   title, url2, 2, Addonicon, Addonfanart, description='')


def Search():
    string = ''
    SearchUrl = ('https://watch.hikaritv.xyz/search?keyword=%s')
    keyboard = xbmc.Keyboard(
        string, '[COLOR magenta][B]What Would You Like To Search For?[/B][/COLOR]')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string) > 1:
            string = string.replace(' ', '+')
            Search_url = (SearchUrl % string)
            filter_search(Search_url)
        else:
            dialog.notification(
                AddonTitle, '[COLOR gold]No Term Entered[/COLOR]', Addonicon, 2500)
    else:
        dialog.notification(
            AddonTitle, '[COLOR gold]Search Cancelled[/COLOR]', Addonicon, 2500)


def filter_search(url):
    base_domain = 'https://watch.hikaritv.xyz'
    link = requests.get(url, headers=get_headers()).text
    soup = BeautifulSoup(link, "html.parser")
    data = soup.find_all('div', class_={'film-detail'})
    for i in data:
        title = i.a.text.strip()
        url2 = i.a['href']
        types = i.find('span', class_={'fdi-item'}).text.strip()
        if url2.startswith('/'):
            url2 = base_domain+url2
        else:
            if not base_domain in url2:
                url2 = base_domain+'/'+url2
        if types.lower() == 'tv':
            addLink('[COLOR magenta][B]%s[/COLOR][/B]' %
                    title, url2, 4, Addonicon, Addonfanart, description='')
        else:
            addLink('[COLOR magenta][B]%s[/COLOR][/B]' %
                    title, url2, 30, Addonicon, Addonfanart, description='')


def MainContent(url):
    name = ''
    base_domain = 'https://watch.hikaritv.xyz'
    if '/ajax' in url:
        link = requests.get(url, headers=get_headers()).json()
    else:
        link = requests.get(url, headers=get_headers()).text
    data = str(link)
    data = data.encode('ascii', 'ignore').decode('ascii')
    soup = BeautifulSoup(data, "html.parser")
    content = soup.find_all('div', class_={'flw-item'})
    for i in content:
        title = i.h3.a.text.strip().replace('\\n', '').strip()
        url2 = i.a['href']
        try:
            icon = i.img['data-src']
        except:
            icon = i.img['src']
        if url2.startswith('/'):
            url2 = base_domain+url2
        else:
            if not base_domain in url2:
                url2 = base_domain+'/'+url2
        addStandardLink('[COLOR magenta][B]%s[/COLOR][/B]' %
                        title, url2, 30, icon, Addonfanart, description='')
    try:
        Getpage = url.split('page=')[-1]
        BasePage = url.rsplit('page=', 1)[0]
        GenNext = int(Getpage) + 1
        NextPage = ('%spage=%s' % (BasePage, GenNext))
        addDir('[COLOR gold][B]Next Page -->[/COLOR][/B]',
               NextPage, 2, Addonicon, Addonfanart, 'Next Page')
    except:
        pass
    if '/search/' in url and name == '':
        name = 'Sorry No Items Found'
        addLink('[COLOR magenta][B]%s[/COLOR][/B]' %
                name, 'url2', 9999, Addonicon, Addonfanart, description='')


def MainContentShows(url):
    if '/ajax' in url:
        link = requests.get(url, headers=get_headers()).json()
    else:
        link = requests.get(url, headers=get_headers()).text
    name = ''
    base_domain = 'https://watch.hikaritv.xyz'
    data = str(link)
    data = data.encode('ascii', 'ignore').decode('ascii')
    soup = BeautifulSoup(data, "html.parser")
    content = soup.find_all('div', class_={'flw-item'})
    for i in content:
        title = i.h3.a.text.strip().replace('\\n', '').strip()
        url2 = i.a['href']
        try:
            icon = i.img['data-src']
        except:
            icon = i.img['src']
        if url2.startswith('/'):
            url2 = base_domain+url2
        else:
            if not base_domain in url2:
                url2 = base_domain+'/'+url2
        addStandardLink('[COLOR magenta][B]%s[/COLOR][/B]' %
                        title, url2, 4, icon, Addonfanart, description='')
    try:
        Getpage = url.split('page=')[-1]
        BasePage = url.rsplit('page=', 1)[0]
        GenNext = int(Getpage) + 1
        NextPage = ('%spage=%s' % (BasePage, GenNext))
        addDir('[COLOR gold][B]Next Page -->[/COLOR][/B]',
               NextPage, 3, Addonicon, Addonfanart, 'Next Page')
    except:
        pass


def Get_Show_Epi(name, url, iconimage):
    names = []
    srcs = []
    epi_ajax_url = 'https://watch.hikaritv.xyz/ajax/episodelist/%s'
    uid_pattern = r'''uid=(.*?)&'''
    link = requests.get(url, headers=get_headers()).text
    get_uid = re.findall(uid_pattern, link)[0]
    link2 = requests.get(epi_ajax_url % get_uid, headers=get_headers()).json()
    soup = BeautifulSoup(str(link2), "html.parser")
    data = soup.find_all('a', id={'getembed'})
    if len(data) < 5:
        pattern_epi = r'''title=['"](.*?)['"].*?number=['"](.*?)['"].*?id=['"](.*?)['"]'''
        get_epis = re.findall(pattern_epi, str(link2), flags=re.DOTALL)
        for title, epi, show_id in get_epis:
            names.append('%s' % title)
            srcs.append(show_id+'|'+epi)
    else:
        for i in data:
            title = i['title']
            epi = re.findall(r'''ep-item-(.*?)['"]''', str(i))[0]
            names.append('%s' % title)
            srcs.append(get_uid+'|'+epi)
    selected = dialog.select('Select an Episode.', names)
    if selected < 0:
        dialog.notification(
            AddonTitle, '[COLOR yellow]No Source Selected[/COLOR]', Addonicon, 2500)
        quit()
    else:
        get_sources = names[selected]
        shows_id = srcs[selected]
    Get_Sources_Epis(get_sources, shows_id, iconimage)


def Get_Sources_Epis(name, url, iconimage):
    dialog.notification(
        AddonTitle, '[COLOR yellow]Getting Sources[/COLOR]', Addonicon, 2500)
    media_id = url.split('|')[0]
    epi_id = url.split('|')[1]
    base_domain = 'https://watch.hikaritv.xyz'
    embed_url = ('https://watch.hikaritv.xyz/ajax/embedserver/%s/%s')
    player_url = ('https://watch.hikaritv.xyz/ajax/embed/%s/%s/%s')
    pattern = r'''getEmbedServer\(.*?,(.*?),(.*?)\)'''
    pattern_emb = r'''embed-([0-9].*?)['"]'''
    get_embed = requests.get(embed_url % (
        media_id, epi_id), headers=get_headers()).json()
    sources = re.findall(pattern_emb, str(get_embed))
    names = []
    srcs = []
    subs = []
    linksfound = 0
    for j in sources:
        get_media = requests.get(player_url % (
            media_id.strip(), epi_id.strip(), j), headers=get_headers()).text
        soup = BeautifulSoup(get_media, "html.parser")
        try:
            source = soup.find('iframe')['src']
            source = source.replace('\\', '').replace('"', '')
            test_source = requests.get(source, headers=get_headers()).text
            find_packed = jsunpack.detect(test_source)
            if find_packed == True:
                unpack_code = jsunpack.unpack(test_source)
                get_playable = re.findall(
                    r'''file:.*?['"](http.+?)['"]''', unpack_code)[0]
                try:
                    get_subs = re.findall(
                        r'''tracks.*?.*?file:.*?['"](http.+?)['"]''', unpack_code, flags=re.DOTALL)[0]
                    subs.append(get_subs)
                except Exception:
                    subs.append('')
                linksfound += 1
                names.append("Link %s" % linksfound)
                srcs.append(get_playable)
        except Exception:
            pass
    if len(names) >= 1:
        selected = dialog.select('Select a link.', names)
        if selected < 0:
            dialog.notification(
                AddonTitle, '[COLOR yellow]No Source Selected[/COLOR]', Addonicon, 2500)
            # quit()
        else:
            url3 = srcs[selected]
            if not 'user-agent' in url3:
                url3 = url3 + \
                    '|User-Agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
            stream_url = url3
            liz = xbmcgui.ListItem(names[selected])
            liz.setProperty('IsPlayable', 'true')
            liz.setPath(stream_url)
            liz.setSubtitles(subs)
            xbmc.Player().play(stream_url, liz, False)
    else:
        dialog.notification(
            AddonTitle, '[COLOR yellow]No Links Found[/COLOR]', Addonicon, 2500)


def Get_Sources(name, url, iconimage):
    dialog.notification(
        AddonTitle, '[COLOR yellow]Hunting Link Now Be Patient[/COLOR]', Addonicon, 2500)
    base_domain = 'https://watch.hikaritv.xyz'
    embed_url = ('https://watch.hikaritv.xyz/ajax/embedserver/%s/%s')
    player_url = ('https://watch.hikaritv.xyz/ajax/embed/%s/%s/%s')
    pattern = r'''getEmbedServer\(.*?,(.*?),(.*?)\)'''
    pattern_emb = r'''embed-([0-9].*?)['"]'''
    if not 'watch?anime=' in url:
        link = requests.get(url, headers=get_headers()).text
        data = str(link)
        data = data.encode('ascii', 'ignore').decode('ascii')
        soup = BeautifulSoup(data, "html.parser")
        get_link = soup.find('div', class_={'film-buttons'})
        get_link = get_link.a['href']
        get_link = base_domain + \
            get_link if get_link.startswith('/') else get_link
    else:
        get_link = url
    link = requests.get(get_link, headers=get_headers()).text
    data = str(link)
    data = data.encode('ascii', 'ignore').decode('ascii')
    find_data = re.findall(pattern, data)
    for media_id, epi_id in find_data:
        get_embed = requests.get(embed_url % (
            media_id.strip(), epi_id.strip()), headers=get_headers()).json()
        sources = re.findall(pattern_emb, str(get_embed))
        names = []
        srcs = []
        subs = []
        linksfound = 0
        for j in sources:
            get_media = requests.get(player_url % (
                media_id.strip(), epi_id.strip(), j), headers=get_headers()).text
            soup = BeautifulSoup(get_media, "html.parser")
            try:
                source = soup.find('iframe')['src']
                source = source.replace('\\', '').replace('"', '')
                test_source = requests.get(source, headers=get_headers()).text
                find_packed = jsunpack.detect(test_source)
                if find_packed == True:
                    unpack_code = jsunpack.unpack(test_source)
                    get_playable = re.findall(
                        r'''file:.*?['"](http.+?)['"]''', unpack_code)[0]
                    try:
                        get_subs = re.findall(
                            r'''tracks.*?.*?file:.*?['"](http.+?)['"]''', unpack_code, flags=re.DOTALL)[0]
                        subs.append(get_subs)
                    except Exception:
                        subs.append('')
                    linksfound += 1
                    names.append("Link %s" % linksfound)
                    srcs.append(get_playable)
            except Exception:
                pass
        if len(names) >= 1:
            selected = dialog.select('Select a link.', names)
            if selected < 0:
                dialog.notification(
                    AddonTitle, '[COLOR yellow]No Source Selected[/COLOR]', Addonicon, 2500)
            else:
                url3 = srcs[selected]
                if not 'user-agent' in url3:
                    url3 = url3 + \
                        '|User-Agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
                stream_url = url3
                liz = xbmcgui.ListItem(names[selected])
                liz.setProperty('IsPlayable', 'true')
                liz.setPath(stream_url)
                liz.setSubtitles(subs)
                xbmc.Player().play(stream_url, liz, False)
        else:
            dialog.notification(
                AddonTitle, '[COLOR yellow]No Links Found[/COLOR]', Addonicon, 2500)


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


def addStandardLink(name, url, mode, iconimage, fanart, description, family=''):

    if not description:
        description = ''
    u = "%s?url=%s&mode=%s&name=%s&iconimage=%s&fanart=%s&description=%s" % (sys.argv[0], quote_plus(
        url), mode, quote_plus(name), quote_plus(iconimage), quote_plus(fanart), quote_plus(description))
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setArt({"thumb": iconimage})
    liz.setInfo('video', {'Plot': description})
    ok = xbmcplugin.addDirectoryItem(handle=int(
        sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def Pin():
    return # StreamFreedom patch
    pin = selfAddon.getSetting('pin')
    if pin == '':
        pin = 'EXPIRED'
    if pin == 'EXPIRED':
        selfAddon.setSetting('pinused', 'False')
        dialog.ok(AddonTitle, "[COLOR yellow]NEW SITE NO MORE POP UPS! Please visit [COLOR lime]https://pinsystem.co.uk[COLOR yellow] to generate an Access Token For [COLOR magenta]FANime[COLOR yellow] then enter it after clicking ok[/COLOR]")
        string = ''
        keyboard = xbmc.Keyboard(
            string, '[COLOR red]Please Enter Pin Generated From Website(Case Sensitive)[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            string = keyboard.getText()
            if len(string) > 1:
                term = string.title()
                selfAddon.setSetting('pin', term)
                Pin()
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
            Pin()
        else:
            registerpin = selfAddon.getSetting('pinused')
            if registerpin == 'False':
                try:
                    requests.get(
                        'https://pinsystem.co.uk/checker.php?code=99999&plugin=FANime').text
                    selfAddon.setSetting('pinused', 'True')
                except:
                    pass
            else:
                pass


params = dict(parse_qsl(sys.argv[2].replace("?", "")))
site = params.get("site", "0")
url = params.get("url", "0")
name = params.get("name", "0")
mode = int(params.get("mode", "0"))
iconimage = params.get("iconimage", "0")
fanart = params.get("fanart", "0")
description = params.get("description", "0")
Pin()
if mode == 0 or url == "0" or len(url) < 1:
    GetMenu()
elif mode == 1:
    GetContent(name, url, iconimage, fanart)
elif mode == 2:
    MainContent(url)
elif mode == 3:
    MainContentShows(url)
elif mode == 4:
    Get_Show_Epi(name, url, iconimage)
elif mode == 5:
    Genres(url)
elif mode == 9:
    Search()
elif mode == 20:
    LinkGetter(name, url, iconimage, description)
elif mode == 30:
    Get_Sources(name, url, iconimage)
elif mode == 99:
    PLAYLINK(name, url, iconimage)
if mode == None or url == None or len(url) < 1:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
else:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
