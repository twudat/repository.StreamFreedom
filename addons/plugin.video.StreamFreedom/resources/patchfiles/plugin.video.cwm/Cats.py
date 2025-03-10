import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import os
import sys
import time
import pyxbmct
import requests
import xbmcvfs
import resolveurl
import importlib
from bs4 import BeautifulSoup
import re
import sqlite3
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
####################################################################
########################### CUSTOM OPTIONS###########################
_addon_id_ = 'plugin.video.cwm'
MainTextColour = 'gold'
AddonTitle = ('[COLOR %s][B]Cum With Me[/B][/COLOR]' % MainTextColour)
####################################################################
_self_ = xbmcaddon.Addon(id=_addon_id_)
_images_ = '/resources/artwork/'
dialog = xbmcgui.Dialog()
Date = time.strftime("%d/%m")
get_setting = _self_.getSetting
set_setting = _self_.setSetting
Skin_Path = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_))
Icon = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'Icon.png'))
AddonIcon = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'Icon.png'))
FanArt = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'Fanart.png'))
Background_Image = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'AddonBG.png'))
Background_Image_Alt = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'AddonBGALT.png'))
AppIcon = xbmcvfs.translatePath(os.path.join(Skin_Path, 'AppIcon.png'))
AppTitle = xbmcvfs.translatePath(os.path.join(Skin_Path, 'AppTitle.gif'))
LiveF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'LiveF1.png'))
LiveNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'LiveNF.png'))
CamF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'CamF1.png'))
CamNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'CamNF.png'))
MoviesF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'MoviesF1.png'))
MoviesNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'MoviesNF.png'))
SitesF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'SitesF1.png'))
SitesNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'SitesNF.png'))
BackF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'BackF1.png'))
BackNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'BackNF.png'))
Frame1NF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'Frame.png'))
Frame1F = xbmcvfs.translatePath(os.path.join(Skin_Path, 'FrameS2.png'))
NextPageNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'NextPageNF.png'))
NextPageF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'NextPageF1.png'))
CatNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'CatNF.png'))
CatF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'CatF1.png'))
FavNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'FavsNF.png'))
FavF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'FavsF.png'))
List_Focused = xbmcvfs.translatePath(os.path.join(Skin_Path, 'ListS.png'))
ActiveF = ''
ActiveNF = ''
DisplayOptions = ''
NextPageUrl = ''
LiveChanUrl = 'https://adult-tv-channels.com/'
MovieUrl = 'https://pandamovies.pw/movies'
CamUrl = 'https://chaturbate.com/api/ts/roomlist/room-list/?enable_recommendations=false&limit=100'
ApiUrl = 'https://pinsystem.co.uk/CumWithMe/api.php'
databases = xbmcvfs.translatePath(os.path.join(
    'special://profile/addon_data/plugin.video.cwm', 'databases'))
cwmdb = xbmcvfs.translatePath(os.path.join(databases, 'cwm.db'))
pDialog = xbmcgui.DialogProgress()


def MainWindow(cat):
    global ActiveF
    global ActiveNF
    global DisplayOptions
    if cat == 'Live':
        ActiveF = LiveF
        ActiveNF = LiveNF
        DisplayOptions = 'Live'
    if cat == 'Cam':
        ActiveF = CamF
        ActiveNF = CamNF
        DisplayOptions = 'Cam'
    if cat == 'Movie':
        ActiveF = MoviesF
        ActiveNF = MoviesNF
        DisplayOptions = 'Movie'
    if cat == 'Sites':
        ActiveF = SitesF
        ActiveNF = SitesNF
        DisplayOptions = 'Sites'
    window = Main('cwm')
    window.doModal()
    del window


def killaddon(self):
    xbmc.executebuiltin("Container.Update(path,replace)")
    xbmc.executebuiltin("ActivateWindow(Home)")
    self.close()


def tick(self):
    time2 = time.strftime("%I:%M %p")
    self.TIME.setLabel(str(time2))


def CloseWindow(self):
    global NextPageUrl
    try:
        if DisplayOptions == 'Cam':
            if self.getFocus() == self.LIST2:
                self.close()
        if self.getFocus() == self.LIST:
            NextPageUrl = ''
            self.close()
        elif self.getFocus() == self.BackButton:
            NextPageUrl = ''
            self.close()
        elif self.getFocus() == self.LIST2:
            NextPageUrl = ''
            self.PerformerImage.setImage(AddonIcon)
            self.button18.setVisible(False)
            self.button17.setVisible(False)
            self.LIST2.reset()
            self.LIST2.setVisible(False)
            self.LIST.setVisible(True)
            self.setFocus(self.LIST)
            self.BackButton.controlRight(self.LIST)
    except:
        NextPageUrl = ''
        self.close()


def LiveChannel(self, url):
    ApiInfo(self)
    global Poster1
    global Poster2
    global Poster3
    global Poster4
    global Poster5
    global Poster6
    global Poster7
    global Poster8
    global Poster9
    global Poster10
    global Poster11
    global Poster12
    global Poster13
    global Poster14
    global Poster15
    global Poster16
    global Stream1
    global Stream2
    global Stream3
    global Stream4
    global Stream5
    global Stream6
    global Stream7
    global Stream8
    global Stream9
    global Stream10
    global Stream11
    global Stream12
    global Stream13
    global Stream14
    global Stream15
    global Stream16
    images = []
    urls = []
    # url = 'https://adult-tv-channels.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
    link = requests.get(url, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('figure', class_={'entry-item-thumb'})
    for i in data:
        image = i.img['src']
        link = i.a['href']
        urls.append(link)
        images.append(image)
    try:
        Poster1 = images[0]
    except:
        Poster1 = ''
    try:
        Stream1 = urls[0]
    except:
        Stream1 = ''
    try:
        Poster2 = images[1]
    except:
        Poster2 = ''
    try:
        Stream2 = urls[1]
    except:
        Stream2 = ''
    try:
        Poster3 = images[2]
    except:
        Poster3 = ''
    try:
        Stream3 = urls[2]
    except:
        Stream3 = ''
    try:
        Poster4 = images[3]
    except:
        Poster4 = ''
    try:
        Stream4 = urls[3]
    except:
        Stream4 = ''
    try:
        Poster5 = images[4]
    except:
        Poster5 = ''
    try:
        Stream5 = urls[4]
    except:
        Stream5 = ''
    try:
        Poster6 = images[5]
    except:
        Poster6 = ''
    try:
        Stream6 = urls[5]
    except:
        Stream6 = ''
    try:
        Poster7 = images[6]
    except:
        Poster7 = ''
    try:
        Stream7 = urls[6]
    except:
        Stream7 = ''
    try:
        Poster8 = images[7]
    except:
        Poster8 = ''
    try:
        Stream8 = urls[7]
    except:
        Stream8 = ''
    try:
        Poster9 = images[8]
    except:
        Poster9 = ''
    try:
        Stream9 = urls[8]
    except:
        Stream9 = ''
    try:
        Poster10 = images[9]
    except:
        Poster10 = ''
    try:
        Stream10 = urls[9]
    except:
        Stream10 = ''
    try:
        Poster11 = images[10]
    except:
        Poster11 = ''
    try:
        Stream11 = urls[10]
    except:
        Stream11 = ''
    try:
        Poster12 = images[11]
    except:
        Poster12 = ''
    try:
        Stream12 = urls[11]
    except:
        Stream12 = ''
    try:
        Poster13 = images[12]
    except:
        Poster13 = ''
    try:
        Stream13 = urls[12]
    except:
        Stream13 = ''
    try:
        Poster14 = images[13]
    except:
        Poster14 = ''
    try:
        Stream14 = urls[13]
    except:
        Stream14 = ''
    try:
        Poster15 = images[14]
    except:
        Poster15 = ''
    try:
        Stream15 = urls[14]
    except:
        Stream15 = ''
    try:
        Poster16 = images[15]
    except:
        Poster16 = ''
    try:
        Stream16 = urls[15]
    except:
        Stream16 = ''

    Channel1 = pyxbmct.Image(Poster1)
    self.placeControl(Channel1, 23, 15, 28, 5)
    Channel2 = pyxbmct.Image(Poster2)
    self.placeControl(Channel2, 23, 23, 28, 5)
    Channel3 = pyxbmct.Image(Poster3)
    self.placeControl(Channel3, 23, 31, 28, 5)
    Channel4 = pyxbmct.Image(Poster4)
    self.placeControl(Channel4, 23, 39, 28, 5)

    Channel5 = pyxbmct.Image(Poster5)
    self.placeControl(Channel5, 53, 15, 28, 5)
    Channel6 = pyxbmct.Image(Poster6)
    self.placeControl(Channel6, 53, 23, 28, 5)
    Channel7 = pyxbmct.Image(Poster7)
    self.placeControl(Channel7, 53, 31, 28, 5)
    Channel8 = pyxbmct.Image(Poster8)
    self.placeControl(Channel8, 53, 39, 28, 5)

    Channel9 = pyxbmct.Image(Poster9)
    self.placeControl(Channel9, 83, 15, 28, 5)
    Channel10 = pyxbmct.Image(Poster10)
    self.placeControl(Channel10, 83, 23, 28, 5)
    Channel11 = pyxbmct.Image(Poster11)
    self.placeControl(Channel11, 83, 31, 28, 5)
    Channel12 = pyxbmct.Image(Poster12)
    self.placeControl(Channel12, 83, 39, 28, 5)

    Channel13 = pyxbmct.Image(Poster13)
    self.placeControl(Channel13, 113, 15, 28, 5)
    Channel14 = pyxbmct.Image(Poster14)
    self.placeControl(Channel14, 113, 23, 28, 5)
    Channel15 = pyxbmct.Image(Poster15)
    self.placeControl(Channel15, 113, 31, 28, 5)
    Channel16 = pyxbmct.Image(Poster16)
    self.placeControl(Channel16, 113, 39, 28, 5)


def Movies(self, url):
    ApiInfo(self)
    global Poster1
    global Poster2
    global Poster3
    global Poster4
    global Poster5
    global Poster6
    global Poster7
    global Poster8
    global Poster9
    global Poster10
    global Poster11
    global Poster12
    global Poster13
    global Poster14
    global Poster15
    global Poster16
    global Stream1
    global Stream2
    global Stream3
    global Stream4
    global Stream5
    global Stream6
    global Stream7
    global Stream8
    global Stream9
    global Stream10
    global Stream11
    global Stream12
    global Stream13
    global Stream14
    global Stream15
    global Stream16
    global Description1
    global Description2
    global Description3
    global Description4
    global Description5
    global Description6
    global Description7
    global Description8
    global Description9
    global Description10
    global Description11
    global Description12
    global Description13
    global Description14
    global Description15
    global Description16
    images = []
    urls = []
    descs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
    link = requests.get(url, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('div', class_={'ml-item'})
    for i in data:
        link = i.a['href']
        image = i.img['data-lazy-src']
        desc = i.find('p', class_={'f-desc'}).text.strip()
        if desc == '':
            desc = 'No Description available'
        desc = ('[COLOR magenta]%s[/COLOR]' % desc)
        urls.append(link)
        images.append(image)
        descs.append(desc)
    try:
        Poster1 = images[0]
    except:
        Poster1 = ''
    try:
        Stream1 = urls[0]
    except:
        Stream1 = ''
    try:
        Poster2 = images[1]
    except:
        Poster2 = ''
    try:
        Stream2 = urls[1]
    except:
        Stream2 = ''
    try:
        Poster3 = images[2]
    except:
        Poster3 = ''
    try:
        Stream3 = urls[2]
    except:
        Stream3 = ''
    try:
        Poster4 = images[3]
    except:
        Poster4 = ''
    try:
        Stream4 = urls[3]
    except:
        Stream4 = ''
    try:
        Poster5 = images[4]
    except:
        Poster5 = ''
    try:
        Stream5 = urls[4]
    except:
        Stream5 = ''
    try:
        Poster6 = images[5]
    except:
        Poster6 = ''
    try:
        Stream6 = urls[6]
    except:
        Stream6 = ''
    try:
        Poster7 = images[6]
    except:
        Poster7 = ''
    try:
        Stream7 = urls[6]
    except:
        Stream7 = ''
    try:
        Poster8 = images[7]
    except:
        Poster8 = ''
    try:
        Stream8 = urls[7]
    except:
        Stream8 = ''
    try:
        Poster9 = images[8]
    except:
        Poster9 = ''
    try:
        Stream9 = urls[8]
    except:
        Stream9 = ''
    try:
        Poster10 = images[9]
    except:
        Poster10 = ''
    try:
        Stream10 = urls[9]
    except:
        Stream10 = ''
    try:
        Poster11 = images[10]
    except:
        Poster11 = ''
    try:
        Stream11 = urls[10]
    except:
        Stream11 = ''
    try:
        Poster12 = images[11]
    except:
        Poster12 = ''
    try:
        Stream12 = urls[11]
    except:
        Stream12 = ''
    try:
        Poster13 = images[12]
    except:
        Poster13 = ''
    try:
        Stream13 = urls[12]
    except:
        Stream13 = ''
    try:
        Poster14 = images[13]
    except:
        Poster14 = ''
    try:
        Stream14 = urls[13]
    except:
        Stream14 = ''
    try:
        Poster15 = images[14]
    except:
        Poster15 = ''
    try:
        Stream15 = urls[14]
    except:
        Stream15 = ''
    try:
        Poster16 = images[15]
    except:
        Poster16 = ''
    try:
        Stream16 = urls[15]
    except:
        Stream16 = ''
    try:
        Description1 = descs[0]
    except:
        Description1 = ''
    try:
        Description2 = descs[1]
    except:
        Description2 = ''
    try:
        Description3 = descs[2]
    except:
        Description3 = ''
    try:
        Description4 = descs[3]
    except:
        Description4 = ''
    try:
        Description5 = descs[4]
    except:
        Description5 = ''
    try:
        Description6 = descs[5]
    except:
        Description6 = ''
    try:
        Description7 = descs[6]
    except:
        Description7 = ''
    try:
        Description8 = descs[7]
    except:
        Description8 = ''
    try:
        Description9 = descs[8]
    except:
        Description9 = ''
    try:
        Description10 = descs[9]
    except:
        Description10 = ''
    try:
        Description11 = descs[10]
    except:
        Description11 = ''
    try:
        Description12 = descs[11]
    except:
        Description12 = ''
    try:
        Description13 = descs[12]
    except:
        Description13 = ''
    try:
        Description14 = descs[13]
    except:
        Description14 = ''
    try:
        Description15 = descs[14]
    except:
        Description15 = ''
    try:
        Description16 = descs[15]
    except:
        Description16 = ''

    Channel1 = pyxbmct.Image(Poster1)
    self.placeControl(Channel1, 23, 15, 28, 5)
    Channel2 = pyxbmct.Image(Poster2)
    self.placeControl(Channel2, 23, 23, 28, 5)
    Channel3 = pyxbmct.Image(Poster3)
    self.placeControl(Channel3, 23, 31, 28, 5)
    Channel4 = pyxbmct.Image(Poster4)
    self.placeControl(Channel4, 23, 39, 28, 5)

    Channel5 = pyxbmct.Image(Poster5)
    self.placeControl(Channel5, 53, 15, 28, 5)
    Channel6 = pyxbmct.Image(Poster6)
    self.placeControl(Channel6, 53, 23, 28, 5)
    Channel7 = pyxbmct.Image(Poster7)
    self.placeControl(Channel7, 53, 31, 28, 5)
    Channel8 = pyxbmct.Image(Poster8)
    self.placeControl(Channel8, 53, 39, 28, 5)

    Channel9 = pyxbmct.Image(Poster9)
    self.placeControl(Channel9, 83, 15, 28, 5)
    Channel10 = pyxbmct.Image(Poster10)
    self.placeControl(Channel10, 83, 23, 28, 5)
    Channel11 = pyxbmct.Image(Poster11)
    self.placeControl(Channel11, 83, 31, 28, 5)
    Channel12 = pyxbmct.Image(Poster12)
    self.placeControl(Channel12, 83, 39, 28, 5)

    Channel13 = pyxbmct.Image(Poster13)
    self.placeControl(Channel13, 113, 15, 28, 5)
    Channel14 = pyxbmct.Image(Poster14)
    self.placeControl(Channel14, 113, 23, 28, 5)
    Channel15 = pyxbmct.Image(Poster15)
    self.placeControl(Channel15, 113, 31, 28, 5)
    Channel16 = pyxbmct.Image(Poster16)
    self.placeControl(Channel16, 113, 39, 28, 5)


def Player(url, iconimage):
    dialog.notification(
        AddonTitle, '[COLOR pink]Sourcing Wank Content Now[/COLOR]', AddonIcon, 2500)
    hmf = resolveurl.HostedMediaFile(url)
    if hmf.valid_url():
        link = hmf.resolve()
        liz = xbmcgui.ListItem('Cum With Me')
        liz.setArt({"thumb": iconimage})
        liz.setPath(link)
        xbmc.Player().play(link, liz, False)
    else:
        stream_url = url  # +'&verifypeer=false'
        liz = xbmcgui.ListItem('Cum With Me')
        liz.setArt({"thumb": iconimage})
        liz.setProperty('IsPlayable', 'true')
        liz.setPath(stream_url)
        xbmc.Player().play(stream_url, liz, False)
        quit()


def ResolveLive(self, image, media):
    ApiInfo(self)
    BaseUrl = 'https://adult-tv-channels.com'
    link = requests.get(media, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    iframe = soup.find('iframe')['src']
    # dialog.ok("IFRAME",str(iframe))
    if not BaseUrl in iframe:
        iframe = BaseUrl+iframe
    headers.update({'Referer': media})
    link2 = requests.get(iframe, headers=headers).text
    pattern = r'''file:['"](.*?)['"]'''
    source = re.findall(pattern, link2)[0]
    source = ('%s|Referer=%s' % (source, iframe))
    # dialog.ok("SOURXE",str(source))
    Player(source, image)


def ResolveMovie(self, image, media):
    ApiInfo(self)
    link = requests.get(media, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find('div', id={'pettabs'})
    linksfound = 0
    streamname = []
    streamurl = []
    for links in data.find_all('a'):
        media = links['href']
        hmf = resolveurl.HostedMediaFile(media)
        if hmf.valid_url():
            linksfound += 1
            title = ('Link %s' % linksfound)
            streamname.append(title)
            streamurl.append(media)
    if linksfound == 0:
        dialog.notification(
            AddonTitle, "[COLOR red][B]Sorry, No Links Found![/B][/COLOR]", AddonIcon, 5000)
        quit()
    else:
        select = dialog.select('Choose A Source', streamname)
        if select < 0:
            quit()
        Player(streamurl[select], image)


def NextPage(self, url, site):
    # dialog.ok("NextPage",str(url))
    ApiInfo(self)
    global NextPageUrl
    if DisplayOptions == 'Live':
        if NextPageUrl == '':
            NextPageUrl = 'https://adult-tv-channels.com/page/2/'
            LiveChannel(self, NextPageUrl)
        else:
            NextPageUrl = NextPageUrl.split('/')[-2]
            NewNextPageUrl = int(NextPageUrl) + 1
            NextPageUrl = (
                'https://adult-tv-channels.com/page/%s/' % NewNextPageUrl)
            LiveChannel(self, NextPageUrl)
    if DisplayOptions == 'Movie':
        if NextPageUrl == '':
            NextPageUrl = 'https://pandamovies.pw/movies/page/2/'
            Movies(self, NextPageUrl)
        else:
            if '/director/' in NextPageUrl:
                NextPageUrl = NextPageUrl.split('/')[-1]
                NewNextPageUrl = int(NextPageUrl) + 1
                url = url.split('/page/')[0]
                NextPageUrl = ('%s/page/%s' % (url, NewNextPageUrl))
                Movies(self, NextPageUrl)
            else:
                NextPageUrl = NextPageUrl.split('/')[-2]
                NewNextPageUrl = int(NextPageUrl) + 1
                NextPageUrl = (
                    'https://pandamovies.pw/movies/page/%s/' % NewNextPageUrl)
                Movies(self, NextPageUrl)
    if DisplayOptions == 'Cam':
        if NextPageUrl == '':
            NextPageUrl = 'https://chaturbate.com/api/ts/roomlist/room-list/?enable_recommendations=false&limit=100&offset=100'
            Cams(self, NextPageUrl)
        else:
            if 'offset=' in NextPageUrl:
                NextPageUrl = url.split('offset=')[-1]
                NewNextPageUrl = int(NextPageUrl) + 100
                first = url.split('offset=')[0]
                NextPageUrl = ('%soffset=%s' % (first, NewNextPageUrl))
                # xbmc.log("NEXTPAGE ::: %s" % NextPageUrl, level=xbmc.LOGINFO)
                Cams(self, NextPageUrl)
            else:
                # dialog.ok("IN","ELSE")
                quit()
                NextPageUrl = NextPageUrl.split('=')[-1]
                NewNextPageUrl = int(NextPageUrl) + 1
                NextPageUrl = ('https://chaturbate.com/?page=%s' %
                               NewNextPageUrl)
                Cams(self, NextPageUrl)
    if DisplayOptions == 'Sites':
        from scrapers import sources
        _sources = sources()
        for source in _sources:
            if site[0] in source[0]:
                getnext = source[1].GetNextPage(url)
                NextPageUrl = getnext
                GetSiteUrl(self, site, getnext)


def GetMovieCats(self, MovieUrl):
    ApiInfo(self)
    global NextPageUrl
    link = requests.get(MovieUrl, headers=headers).text
    streamname = []
    streamurl = []
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find('li', id={'menu-item-23'})
    for i in data.find_all('a'):
        if not '#' in i['href']:
            name = i.text
            url2 = i['href']
            streamname.append(name)
            streamurl.append(url2)
    select = dialog.select('Choose an Studio', streamname)
    if select < 0:
        quit()
    else:
        NextPageUrl = ('%s/page/1' % streamurl[select])
        Movies(self, streamurl[select])


def Cams(self, url):
    CheckMonitor = get_setting('Monitor')
    self.setFocus(self.LIST)
    self.LIST2.reset()
    self.LIST2.setVisible(False)
    self.LIST.setVisible(True)
    global camimage
    global camurl
    global camdesc
    global camname
    defaulturl = 'https://chaturbate.com'
    camimage = []
    camurl = []
    camdesc = []
    camname = []
    self.LIST.reset()
    camimage.append(AddonIcon)
    camurl.append('')
    camdesc.append('')
    camname.append('')
    self.LIST.addItem('[COLOR magenta]Live Cams From Chaturbate[/COLOR]')
    if CheckMonitor == 'true':
        status = '[COLOR lime]ON[/COLOR]'
        camurl.append('monitoron')
    else:
        status = '[COLOR red]OFF[/COLOR]'
        camurl.append('monitoroff')
    camimage.append(AddonIcon)
    camdesc.append('')
    camname.append('')
    self.LIST.addItem(
        '[COLOR magenta]Favourite Performer Monitor Status : %s[/COLOR]' % status)
    link = requests.get(url, headers=headers).json()
    # soup = BeautifulSoup(link, 'html.parser')
    data = link['rooms']
    for i in data:
        pname = i['username']
        img = i['img']
        href = ('https://chaturbate.com/%s/' % pname)
        if not defaulturl in href:
            href = defaulturl+href
        age = i['display_age']
        if len(str(age)) >= 3:
            age = '?'
        desc = i['subject']
        views = i['num_users']
        camname.append(pname.title())
        camimage.append(img)
        camurl.append(href)
        camdesc.append('Age : %s\n\nViewers : %s\n\n%s' % (age, views, desc))
        self.LIST.addItem(pname.title())


def PlayCam(self, mode):
    ApiInfo(self)
    listpos = self.LIST.getSelectedPosition()
    media = camurl[listpos]
    if media == 'monitoron':
        xbmcaddon.Addon().openSettings()
    elif media == 'monitoroff':
        xbmcaddon.Addon().openSettings()
    else:
        if mode == 'list':
            whattodo = dialog.yesnocustom(AddonTitle, 'Select an option', yeslabel='View Cam',
                                          nolabel='Add to favs', customlabel='Close', defaultbutton=11)
            if whattodo == 0:
                AddCamToFavs(self)
            elif whattodo == 2:
                quit()
            else:
                pattern = r'''hls_source.+(http.*?m3u8)'''
                link = requests.get(media, headers=headers).text
                source = re.findall(pattern, link, flags=re.DOTALL)[0]
                source = source.replace('u002D', '-').replace('\-', '-')
                Player(source, camimage[listpos])
        elif mode == 'fav':
            whattodo = dialog.yesnocustom(AddonTitle, 'Select an option', yeslabel='View Cam',
                                          nolabel='Remove to favs', customlabel='Close', defaultbutton=11)
            if whattodo == 0:
                RemoveCamFavs(self)
            elif whattodo == 2:
                quit()
            else:
                listpos = self.LIST2.getSelectedPosition()
                media = camurl[listpos]
                pattern = r'''hls_source.+(http.*?m3u8)'''
                link = requests.get(media, headers=headers).text
                source = re.findall(pattern, link, flags=re.DOTALL)[0]
                source = source.replace('u002D', '-').replace('\-', '-')
                Player(source, camimage[listpos])


def GetCamCats(self, url):
    global NextPageUrl
    link = requests.get(url, headers=headers).json()
    streamname = []
    streamurl = []
    for i in link['hashtags']:
        cat = i['hashtag']  # .title()
        viewercount = i['viewer_count']
        name = ('%s | Viewer Count : %s' % (cat.title(), viewercount))
        url2 = ('https://chaturbate.com/api/ts/roomlist/room-list/?enable_recommendations=false&hashtags=%s&limit=100&offset=0' % cat)
        streamname.append(name)
        streamurl.append(url2)
    select = dialog.select('Choose an Tag', streamname)
    if select < 0:
        quit()
    else:
        NextPageUrl = streamurl[select]
        Cams(self, streamurl[select])


def Sites(self):
    self.button18.setVisible(False)
    self.button17.setVisible(False)
    global sites
    self.LIST2.reset()
    self.LIST2.setVisible(False)
    sites = []
    sites.append('')
    from scrapers import sources
    _sources = sources()
    self.LIST.addItem('[COLOR magenta]Cum With Me Available Sites[/COLOR]')
    self.LIST.addItem('[COLOR gold]Search All Sites[/COLOR]')
    sites.append('SEARCH')
    for source in _sources:
        sites.append(source)
        self.LIST.addItem(source[0].title())


def GetSiteUrl(self, site, url):
    ApiInfo(self)
    self.LIST2.reset()
    global movimage
    global movurl
    global movdesc
    global movname
    global ActiveSite
    ActiveSite = site
    self.LIST2.setVisible(True)
    self.LIST.setVisible(False)
    self.button18.setVisible(True)
    self.button17.setVisible(True)
    movimage = []
    movurl = []
    movdesc = []
    movname = []
    from scrapers import sources
    _sources = sources()
    data = []
    totalsources = len(_sources)
    percent = 100 / totalsources
    searched = 0
    if 'SEARCH' in site:
        string = ''
        keyboard = xbmc.Keyboard(
            string, '[COLOR magenta]Cum on then, What shall we search for?[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            string = keyboard.getText()
        pDialog.create(AddonTitle, 'Searching for\n%s...' % string)
        for source in _sources:
            searched += 1
            total = searched * percent
            if (pDialog.iscanceled()):
                pDialog.close()
                self.setFocus(self.LIST2)
                quit()
            try:
                if len(string) > 1:
                    getsearch = source[1].SearchSite(string)
                    for info in getsearch:
                        movname.append(info['name'])
                        movimage.append(info['image'])
                        movurl.append(info['url'])
                        self.LIST2.addItem(info['name'])
                pDialog.update(int(total), 'Searching : %s\nQuery: %s\nVideos Found : %s\nSites Searched : %s | %s' % (
                    source[0], string.title(), str(len(movname)), str(searched), str(totalsources)))
            except Exception as c:
                xbmc.log('SCRAPER ERROR : %s ::: %s' %
                         (source, c), xbmc.LOGINFO)
        pDialog.close()
        self.setFocus(self.LIST2)
    else:
        movimage.append(AddonIcon)
        movurl.append('')
        movdesc.append('')
        movname.append('')
        self.LIST2.addItem(
            '[COLOR magenta]Content From %s[/COLOR]' % site[0].upper())
        for source in _sources:
            if site[0] in source[0]:
                getcontent = source[1].MainContent(url)
                for info in getcontent:
                    movname.append(info['name'])
                    movimage.append(info['image'])
                    movurl.append(info['url'])
                    self.LIST2.addItem(info['name'])
        self.setFocus(self.LIST2)


def ResolveSiteMovie(self, site):
    ApiInfo(self)
    listpos = self.LIST2.getSelectedPosition()
    media = movurl[listpos]
    from scrapers import sources
    _sources = sources()
    streamname = []
    streamurl = []
    linksfound = 0
    for source in _sources:
        if site[0] in source[0]:
            resolvelink = source[1].ResolveLink(media)
            for links in resolvelink:
                linksfound += 1
                streamname.append(links['name'])
                streamurl.append(links['url'])
        elif source[0].lower() in media.lower():
            resolvelink = source[1].ResolveLink(media)
            for links in resolvelink:
                linksfound += 1
                streamname.append(links['name'])
                streamurl.append(links['url'])
    if linksfound == 0:
        dialog.notification(
            AddonTitle, "[COLOR red][B]Sorry, No Links Found![/B][/COLOR]", AddonIcon, 5000)
        quit()
    else:
        select = dialog.select('Choose A Source', streamname)
        if select < 0:
            quit()
        Player(streamurl[select], movimage[listpos])


def GetSiteCats(self, site):
    ApiInfo(self)
    global NextPageUrl
    from scrapers import sources
    _sources = sources()
    catname = []
    caturl = []
    catsfound = 0
    for source in _sources:
        if site[0] in source[0]:
            getcats = source[1].GetCats()
            for cat in getcats:
                catsfound += 1
                catname.append(cat['name'])
                caturl.append(cat['url'])
    # dialog.ok("CATSURL",str(caturl))
    if catsfound == 0:
        dialog.notification(
            AddonTitle, "[COLOR red][B]Sorry, No Links Found![/B][/COLOR]", AddonIcon, 5000)
        quit()
    else:
        select = dialog.select('Choose A Catergory', catname)
        if select < 0:
            quit()
        NextPageUrl = caturl[select]
        GetSiteUrl(self, site, caturl[select])


def ApiInfo(self):
    try:
        link = requests.get(ApiUrl).json()
        for data in link:
            usersonline = data['usercount']['Users']
            camsonline = data['usercount']['CamsOnline']
            videos = data['usercount']['Videos']
            self.USERS.setLabel('Current Cummers Online : %s' % usersonline)
            self.CHANNELS.setLabel('Live Cams Available : %s' % camsonline)
            self.MOVIES.setLabel('Movies Available : %s' % videos)
    except:
        pass


def ShowCamFavs(self):
    global camurl
    global camname
    global camimage
    global camdesc
    self.LIST2.reset()
    self.LIST.reset()
    self.LIST2.setVisible(True)
    self.LIST.setVisible(False)
    self.button18.controlUp(self.LIST2)
    self.button19.controlUp(self.LIST2)
    self.button17.controlUp(self.LIST2)
    self.BackButton.controlRight(self.LIST2)
    self.LIST2.controlLeft(self.BackButton)
    self.LIST2.controlRight(self.button17)
    camimage = []
    camurl = []
    camdesc = []
    camname = []
    camimage.append(AddonIcon)
    camurl.append('')
    camdesc.append('')
    camname.append('')
    self.LIST2.addItem('[COLOR magenta]Favourite Cams From Chaturbate[/COLOR]')
    conn = sqlite3.connect(cwmdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM chaturbate")
    e = [u for u in c.fetchall()]
    if len(e) < 1:
        self.LIST2.addItem('[COLOR white]No Favourites Added yet[/COLOR]')
        quit()
    for (name, url, image) in e:
        camname.append(name)
        camurl.append(url)
        camimage.append(image)
        pattern = r'''hls_source.+(http.*?m3u8)'''
        link = requests.get(url, headers=headers).text
        source = re.findall(pattern, link, flags=re.DOTALL)
        if source:
            self.LIST2.addItem(name + '|[COLOR green]Online[/COLOR]')
        else:
            self.LIST2.addItem(name + '|[COLOR red]Offline[/COLOR]')
    conn.close()
    self.setFocus(self.LIST2)


def AddCamToFavs(self):
    listpos = self.LIST.getSelectedPosition()
    media = camurl[listpos]
    name = camname[listpos]
    img = camimage[listpos]
    conn = sqlite3.connect(cwmdb)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO chaturbate VALUES (?,?,?)", (name, media, img))
    conn.commit()
    conn.close()
    dialog.notification(
        AddonTitle, '[COLOR pink]%s Added To Favs & Monitoring[/COLOR]' % name, img, 2500)


def RemoveCamFavs(self):
    listpos = self.LIST2.getSelectedPosition()
    media = camurl[listpos]
    name = camname[listpos]
    img = camimage[listpos]
    conn = sqlite3.connect(cwmdb)
    c = conn.cursor()
    c.execute("DELETE FROM chaturbate WHERE url = '%s'" % media)
    conn.commit()
    conn.close()
    dialog.notification(
        AddonTitle, '[COLOR pink]%s Removed from Favs & Monitoring[/COLOR]' % name, img, 2500)
    ShowCamFavs(self)


class Main(pyxbmct.AddonFullWindow):
    xbmc.executebuiltin("Dialog.Close(busydialog)")

    def __init__(self, title='cwm'):
        super(Main, self).__init__(title)
        self.setGeometry(1280, 720, 150, 50)
        if DisplayOptions == 'Live' or DisplayOptions == 'Movie':
            self.main_bg_img = Background_Image
            self.main_bg = xbmcgui.ControlImage(
                0, 0, 1280, 720, self.main_bg_img)
            self.main_bg.setImage(Background_Image)
            self.addControl(self.main_bg)
        else:
            self.main_bg_img = Background_Image_Alt
            self.main_bg = xbmcgui.ControlImage(
                0, 0, 1280, 720, self.main_bg_img)
            self.main_bg.setImage(Background_Image_Alt)
            self.addControl(self.main_bg)
        self.main_bg = xbmcgui.ControlImage(0, 0, 1280, 720, self.main_bg_img)
        self.addControl(self.main_bg)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, lambda: CloseWindow(self))
        AppLogo = pyxbmct.Image(AppIcon)
        self.placeControl(AppLogo, -10, 45, 30, 6)
        AppHeader = pyxbmct.Image(AppTitle)
        self.placeControl(AppHeader, -10, 0, 18, 20)
        ApiInfo(self)
        if DisplayOptions == 'Live':
            LiveChannel(self, LiveChanUrl)
            self.connect(self.button1, lambda: ResolveLive(
                self, Poster1, Stream1))
            self.connect(self.button2, lambda: ResolveLive(
                self, Poster2, Stream2))
            self.connect(self.button3, lambda: ResolveLive(
                self, Poster3, Stream3))
            self.connect(self.button4, lambda: ResolveLive(
                self, Poster4, Stream4))
            self.connect(self.button5, lambda: ResolveLive(
                self, Poster5, Stream5))
            self.connect(self.button6, lambda: ResolveLive(
                self, Poster6, Stream6))
            self.connect(self.button7, lambda: ResolveLive(
                self, Poster7, Stream7))
            self.connect(self.button8, lambda: ResolveLive(
                self, Poster8, Stream8))
            self.connect(self.button9, lambda: ResolveLive(
                self, Poster9, Stream9))
            self.connect(self.button10, lambda: ResolveLive(
                self, Poster10, Stream10))
            self.connect(self.button11, lambda: ResolveLive(
                self, Poster11, Stream11))
            self.connect(self.button12, lambda: ResolveLive(
                self, Poster12, Stream12))
            self.connect(self.button13, lambda: ResolveLive(
                self, Poster13, Stream13))
            self.connect(self.button14, lambda: ResolveLive(
                self, Poster14, Stream14))
            self.connect(self.button15, lambda: ResolveLive(
                self, Poster15, Stream15))
            self.connect(self.button16, lambda: ResolveLive(
                self, Poster16, Stream16))
            self.connect(self.button17, lambda: NextPage(self, '', ''))
            self.setFocus(self.button1)
        if DisplayOptions == 'Movie':
            Movies(self, MovieUrl)
            self.connect(self.button1, lambda: ResolveMovie(
                self, Poster1, Stream1))
            self.connect(self.button2, lambda: ResolveMovie(
                self, Poster2, Stream2))
            self.connect(self.button3, lambda: ResolveMovie(
                self, Poster3, Stream3))
            self.connect(self.button4, lambda: ResolveMovie(
                self, Poster4, Stream4))
            self.connect(self.button5, lambda: ResolveMovie(
                self, Poster5, Stream5))
            self.connect(self.button6, lambda: ResolveMovie(
                self, Poster6, Stream6))
            self.connect(self.button7, lambda: ResolveMovie(
                self, Poster7, Stream7))
            self.connect(self.button8, lambda: ResolveMovie(
                self, Poster8, Stream8))
            self.connect(self.button9, lambda: ResolveMovie(
                self, Poster9, Stream9))
            self.connect(self.button10, lambda: ResolveMovie(
                self, Poster10, Stream10))
            self.connect(self.button11, lambda: ResolveMovie(
                self, Poster11, Stream11))
            self.connect(self.button12, lambda: ResolveMovie(
                self, Poster12, Stream12))
            self.connect(self.button13, lambda: ResolveMovie(
                self, Poster13, Stream13))
            self.connect(self.button14, lambda: ResolveMovie(
                self, Poster14, Stream14))
            self.connect(self.button15, lambda: ResolveMovie(
                self, Poster15, Stream15))
            self.connect(self.button16, lambda: ResolveMovie(
                self, Poster16, Stream16))
            self.connect(self.button17, lambda: NextPage(
                self, NextPageUrl, ''))
            self.connect(self.button18, lambda: GetMovieCats(self, MovieUrl))
            self.setFocus(self.button1)
        if DisplayOptions == 'Cam':
            Cams(self, CamUrl)
            self.PerformerImage = pyxbmct.Image(AddonIcon)
            self.placeControl(self.PerformerImage, 82, 39, 54, 9)
            self.connect(self.LIST, lambda: PlayCam(self, 'list'))
            self.connect(self.LIST2, lambda: PlayCam(self, 'fav'))
            self.connect(self.button17, lambda: NextPage(
                self, NextPageUrl, ''))
            self.connect(self.button18, lambda: GetCamCats(
                self, 'https://chaturbate.com/api/ts/hashtags/tag-table-data/?sort=&page=1&g=&limit=100'))
            self.connect(self.button19, lambda: ShowCamFavs(self))
            self.setFocus(self.LIST)
        if DisplayOptions == 'Sites':
            Sites(self)
            self.connect(self.LIST, lambda: GetSiteUrl(self, site, ''))
            self.connect(
                self.LIST2, lambda: ResolveSiteMovie(self, ActiveSite))
            self.PerformerImage = pyxbmct.Image(AddonIcon)
            self.placeControl(self.PerformerImage, 82, 39, 54, 9)
            self.setFocus(self.LIST)
            self.connect(self.button18, lambda: GetSiteCats(self, site))
            self.connect(self.button17, lambda: NextPage(
                self, NextPageUrl, site))

    def set_info_controls(self):
        self.TIME = pyxbmct.Label('', textColor='0xFFFFFFFF', font='font14')
        self.USERS = pyxbmct.Label('', textColor='0xFFFFFFFF', font='font14')
        self.CHANNELS = pyxbmct.Label(
            '', textColor='0xFFFFFFFF', font='font14')
        self.MOVIES = pyxbmct.Label('', textColor='0xFFFFFFFF', font='font14')
        self.placeControl(self.TIME, 158, 47, 12, 10)
        self.placeControl(self.USERS, 158, 0, 12, 20)
        self.placeControl(self.CHANNELS, 150, 0, 12, 20)
        self.placeControl(self.MOVIES, 142, 0, 12, 20)
        time2 = time.strftime("%I:%M %p")
        self.TIME.setLabel(str(time2))
        self.USERS.setLabel('Current Cummers Online : ')
        self.CHANNELS.setLabel('Live Cams Available : ')
        self.MOVIES.setLabel('Movies Available : ')
    # def onAction(self, action):
        # if action == KEY_MOUSE_RIGHTCLICK:
        # dialog.ok("YOU","Long CLICKED")

    def set_active_controls(self):
        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.list_update)
        # T L H W
        if DisplayOptions == 'Live':
            self.button1 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button1, 22, 14, 30, 7)
            self.button2 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button2, 22, 22, 30, 7)
            self.button3 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button3, 22, 30, 30, 7)
            self.button4 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button4, 22, 38, 30, 7)
            # 2nd Row
            self.button5 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button5, 52, 14, 30, 7)
            self.button6 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button6, 52, 22, 30, 7)
            self.button7 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button7, 52, 30, 30, 7)
            self.button8 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button8, 52, 38, 30, 7)
            # 3rd Row
            self.button9 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button9, 82, 14, 30, 7)
            self.button10 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button10, 82, 22, 30, 7)
            self.button11 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button11, 82, 30, 30, 7)
            self.button12 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button12, 82, 38, 30, 7)
            # 4th Row
            self.button13 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button13, 112, 14, 30, 7)
            self.button14 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button14, 112, 22, 30, 7)
            self.button15 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button15, 112, 30, 30, 7)
            self.button16 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button16, 112, 38, 30, 7)
            self.button17 = pyxbmct.Button(
                '',   focusTexture=NextPageF,   noFocusTexture=NextPageNF)
            self.placeControl(self.button17, 142, 38, 20, 7)
        if DisplayOptions == 'Movie':
            self.button1 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button1, 22, 14, 30, 7)
            self.button2 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button2, 22, 22, 30, 7)
            self.button3 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button3, 22, 30, 30, 7)
            self.button4 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button4, 22, 38, 30, 7)
            # 2nd Row
            self.button5 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button5, 52, 14, 30, 7)
            self.button6 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button6, 52, 22, 30, 7)
            self.button7 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button7, 52, 30, 30, 7)
            self.button8 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button8, 52, 38, 30, 7)
            # 3rd Row
            self.button9 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button9, 82, 14, 30, 7)
            self.button10 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button10, 82, 22, 30, 7)
            self.button11 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button11, 82, 30, 30, 7)
            self.button12 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button12, 82, 38, 30, 7)
            # 4th Row
            self.button13 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button13, 112, 14, 30, 7)
            self.button14 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button14, 112, 22, 30, 7)
            self.button15 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button15, 112, 30, 30, 7)
            self.button16 = pyxbmct.Button(
                '',   focusTexture=Frame1F,   noFocusTexture=Frame1NF)
            self.placeControl(self.button16, 112, 38, 30, 7)
            self.button17 = pyxbmct.Button(
                '',   focusTexture=NextPageF,   noFocusTexture=NextPageNF)
            self.placeControl(self.button17, 142, 38, 20, 7)
            self.button18 = pyxbmct.Button(
                '',   focusTexture=CatF,   noFocusTexture=CatNF)
            self.placeControl(self.button18, 142, 14, 20, 7)
        if DisplayOptions == 'Cam':
            self.LIST = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture='', _imageWidth=10, _imageHeight=10,
                                     _space=-1, _itemHeight=35,  _itemTextXOffset=-5, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
            self.placeControl(self.LIST, 16, 15, 134, 22)
            self.button17 = pyxbmct.Button(
                '',   focusTexture=NextPageF,   noFocusTexture=NextPageNF)
            self.placeControl(self.button17, 142, 32, 20, 7)
            self.button18 = pyxbmct.Button(
                '',   focusTexture=CatF,   noFocusTexture=CatNF)
            self.placeControl(self.button18, 142, 14, 20, 7)
            self.button19 = pyxbmct.Button(
                '',   focusTexture=FavF,   noFocusTexture=FavNF)
            self.placeControl(self.button19, 142, 24, 23, 5)
            self.LIST2 = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture='', _imageWidth=10, _imageHeight=10,
                                      _space=-1, _itemHeight=35,  _itemTextXOffset=-5, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
            self.placeControl(self.LIST2, 16, 15, 134, 22)
        if DisplayOptions == 'Sites':
            self.LIST = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture='', _imageWidth=10, _imageHeight=10,
                                     _space=-1, _itemHeight=35,  _itemTextXOffset=-5, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
            self.placeControl(self.LIST, 16, 15, 134, 22)
            self.LIST2 = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture='', _imageWidth=10, _imageHeight=10,
                                      _space=-1, _itemHeight=35,  _itemTextXOffset=-5, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
            self.placeControl(self.LIST2, 16, 15, 134, 22)
            self.button17 = pyxbmct.Button(
                '',   focusTexture=NextPageF,   noFocusTexture=NextPageNF)
            self.placeControl(self.button17, 142, 31, 20, 7)
            self.button18 = pyxbmct.Button(
                '',   focusTexture=CatF,   noFocusTexture=CatNF)
            self.placeControl(self.button18, 142, 14, 20, 7)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 70, 0, 50, 14)
        self.textbox.autoScroll(1000, 1000, 1000)
        self.ActiveButton = pyxbmct.Button(
            '',   focusTexture=ActiveF,   noFocusTexture=ActiveNF)
        self.placeControl(self.ActiveButton, 10, 0, 30, 12)
        self.BackButton = pyxbmct.Button(
            '',   focusTexture=BackF,   noFocusTexture=BackNF)
        self.placeControl(self.BackButton, 40, 0, 30, 12)
        self.connect(self.BackButton, lambda: CloseWindow(self))

    def set_navigation(self):
        if DisplayOptions == 'Live' or DisplayOptions == 'Movie':
            # LEFT
            self.button1.controlLeft(self.BackButton)
            self.button2.controlLeft(self.button1)
            self.button3.controlLeft(self.button2)
            self.button4.controlLeft(self.button3)

            self.button5.controlLeft(self.BackButton)
            self.button6.controlLeft(self.button5)
            self.button7.controlLeft(self.button6)
            self.button8.controlLeft(self.button7)

            self.button9.controlLeft(self.BackButton)
            self.button10.controlLeft(self.button9)
            self.button11.controlLeft(self.button10)
            self.button12.controlLeft(self.button11)

            self.button13.controlLeft(self.BackButton)
            self.button14.controlLeft(self.button13)
            self.button15.controlLeft(self.button14)
            self.button16.controlLeft(self.button15)
            # RIGHT
            self.button1.controlRight(self.button2)
            self.button2.controlRight(self.button3)
            self.button3.controlRight(self.button4)
            self.button5.controlRight(self.button6)
            self.button6.controlRight(self.button7)
            self.button7.controlRight(self.button8)
            self.button9.controlRight(self.button10)
            self.button10.controlRight(self.button11)
            self.button11.controlRight(self.button12)
            self.button13.controlRight(self.button14)
            self.button14.controlRight(self.button15)
            self.button15.controlRight(self.button16)
            self.BackButton.controlRight(self.button1)
            # UP
            self.button13.controlUp(self.button9)
            self.button9.controlUp(self.button5)
            self.button5.controlUp(self.button1)
            self.button14.controlUp(self.button10)
            self.button10.controlUp(self.button6)
            self.button6.controlUp(self.button2)
            self.button15.controlUp(self.button11)
            self.button11.controlUp(self.button7)
            self.button7.controlUp(self.button3)
            self.button16.controlUp(self.button12)
            self.button12.controlUp(self.button8)
            self.button8.controlUp(self.button4)
            self.button17.controlUp(self.button16)
            # DOWN
            self.button1.controlDown(self.button5)
            self.button5.controlDown(self.button9)
            self.button9.controlDown(self.button13)
            self.button2.controlDown(self.button6)
            self.button6.controlDown(self.button10)
            self.button10.controlDown(self.button14)
            self.button3.controlDown(self.button7)
            self.button7.controlDown(self.button11)
            self.button11.controlDown(self.button15)
            self.button4.controlDown(self.button8)
            self.button8.controlDown(self.button12)
            self.button12.controlDown(self.button16)
            if DisplayOptions == 'Movie':
                self.button13.controlDown(self.button18)
                self.button14.controlDown(self.button18)
                self.button18.controlUp(self.button13)
                self.button18.controlLeft(self.BackButton)
                self.button18.controlRight(self.button17)
                self.button17.controlLeft(self.button18)
            else:
                self.button13.controlDown(self.button17)
                self.button14.controlDown(self.button17)
            self.button15.controlDown(self.button17)
            self.button16.controlDown(self.button17)
        if DisplayOptions == 'Cam':
            # LEFT
            self.LIST.controlLeft(self.BackButton)
            self.LIST2.controlLeft(self.BackButton)
            self.button17.controlLeft(self.button19)
            self.button19.controlLeft(self.button18)
            self.button18.controlLeft(self.BackButton)
            # RIGHT
            self.BackButton.controlRight(self.LIST)
            self.button18.controlRight(self.button19)
            self.button19.controlRight(self.button17)
            self.LIST.controlRight(self.button17)
            self.LIST2.controlRight(self.button17)
            # DOWN
            self.BackButton.controlDown(self.button18)
            # UP
            self.button18.controlUp(self.LIST)
            self.button19.controlUp(self.LIST)
            self.button17.controlUp(self.LIST)
        if DisplayOptions == 'Sites':
            # LEFT
            self.LIST.controlLeft(self.BackButton)
            self.button17.controlLeft(self.button18)
            self.button18.controlLeft(self.BackButton)
            # RIGHT
            self.BackButton.controlRight(self.LIST)
            self.button18.controlRight(self.button17)
            self.LIST.controlRight(self.button17)
            # DOWN
            self.BackButton.controlDown(self.button18)
            # UP
            self.button18.controlUp(self.LIST)
            self.button17.controlUp(self.LIST)
            self.LIST2.controlLeft(self.BackButton)
            self.LIST2.controlRight(self.button17)
            # if self.LIST2 == True: self.BackButton.controlRight(self.LIST2)
            self.button18.controlUp(self.LIST2)
            self.button17.controlUp(self.LIST2)
            # self.BackButton.controlRight(self.LIST2)

    def list_update(self):
        tick(self)
        if DisplayOptions == 'Movie':
            if self.getFocus() == self.button1:
                self.textbox.setText(Description1)
            if self.getFocus() == self.button2:
                self.textbox.setText(Description2)
            if self.getFocus() == self.button3:
                self.textbox.setText(Description3)
            if self.getFocus() == self.button4:
                self.textbox.setText(Description4)
            if self.getFocus() == self.button5:
                self.textbox.setText(Description5)
            if self.getFocus() == self.button6:
                self.textbox.setText(Description6)
            if self.getFocus() == self.button7:
                self.textbox.setText(Description7)
            if self.getFocus() == self.button8:
                self.textbox.setText(Description8)
            if self.getFocus() == self.button9:
                self.textbox.setText(Description9)
            if self.getFocus() == self.button10:
                self.textbox.setText(Description10)
            if self.getFocus() == self.button11:
                self.textbox.setText(Description11)
            if self.getFocus() == self.button12:
                self.textbox.setText(Description12)
            if self.getFocus() == self.button13:
                self.textbox.setText(Description13)
            if self.getFocus() == self.button14:
                self.textbox.setText(Description14)
            if self.getFocus() == self.button15:
                self.textbox.setText(Description15)
            if self.getFocus() == self.button16:
                self.textbox.setText(Description16)
            if self.getFocus() == self.button17:
                self.textbox.setText('[COLOR magenta]Next Page[/COLOR]')
            if self.getFocus() == self.button18:
                self.textbox.setText('[COLOR magenta]Select Category[/COLOR]')
            if self.getFocus() == self.BackButton:
                self.textbox.setText('[COLOR magenta]Go Back[/COLOR]')
        if DisplayOptions == 'Live':
            self.textbox.setText('[COLOR magenta]Due To Source Limits, Only a limted number of channels can be displayed per page,\n'
                                 'More channels maybe available on next page[/COLOR]')
            if self.getFocus() == self.button17:
                self.textbox.setText('[COLOR magenta]Next Page[/COLOR]')
            if self.getFocus() == self.BackButton:
                self.textbox.setText('[COLOR magenta]Go Back[/COLOR]')
        if DisplayOptions == 'Cam':
            # dialog.ok("IN","CAM")
            self.textbox.setText('[COLOR magenta][/COLOR]')
            if self.getFocus() == self.BackButton:
                self.textbox.setText('[COLOR magenta]Go Back[/COLOR]')
            if self.getFocus() == self.button17:
                self.textbox.setText('[COLOR magenta]Next Page[/COLOR]')
            if self.getFocus() == self.button18:
                self.textbox.setText('[COLOR magenta]Select Category[/COLOR]')
            if self.getFocus() == self.LIST:
                listpos = self.LIST.getSelectedPosition()
                desc = camdesc[listpos]
                self.textbox.setText('[COLOR magenta]%s[/COLOR]' % desc)
                setpefimage = camimage[listpos]
                self.PerformerImage.setImage(setpefimage)
            if self.getFocus() == self.LIST2:
                listpos = self.LIST2.getSelectedPosition()
                # desc = camdesc[listpos]
                # self.textbox.setText('[COLOR magenta]%s[/COLOR]' %desc)
                setpefimage = camimage[listpos]
                self.PerformerImage.setImage(setpefimage)
        if DisplayOptions == 'Sites':
            if self.getFocus() == self.LIST:
                global site
                listpos = self.LIST.getSelectedPosition()
                site = sites[listpos]
                self.BackButton.controlRight(self.LIST)
            if self.getFocus() == self.LIST2:
                listpos = self.LIST2.getSelectedPosition()
                try:
                    setpefimage = movimage[listpos]
                except:
                    setpefimage = AddonIcon
                self.PerformerImage.setImage(setpefimage)
                self.BackButton.controlRight(self.LIST2)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=2000',),
                               ('WindowClose', 'effect=fade start=100 end=0 time=1000',)])


if __name__ == '__main__':
    MainWindow()
