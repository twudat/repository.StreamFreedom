#############################################################
#################### START ADDON IMPORTS ####################
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2


import os
import re
import requests
import sys
import time
import pyxbmct
import resolveurl
from bs4 import BeautifulSoup
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
dialog = xbmcgui.Dialog()

#############################################################
#################### SET ADDON ID ###########################
_addon_id_ = 'plugin.video.EntertainMe'
_self_ = xbmcaddon.Addon(id=_addon_id_)
Date = time.strftime("%A %B %d")
AddonTitle = '[B][COLOR red]E[COLOR yellow]ntertain Me[/B][/COLOR]'
dp = xbmcgui.DialogProgress()
icon = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'icon.png'))
Addonicon = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'icon.png'))
#############################################################
#################### SET ADDON THEME DIRECTORY ##############
_theme_ = _self_.getSetting('Theme')
_images_ = '/resources/' + _theme_
#############################################################
#################### SET ADDON THEME IMAGES #################
Background_Image = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'bg.jpg'))
SText = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'searchtxt.png'))
ButtonFrame = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'ButtonFrame.png'))
ButtonFrameS = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'ButtonFrameS.png'))
ButtonMovies = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'Movies_Button.png'))
ButtonMoviesS = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'Movies_ButtonS.png'))
ButtonTvShows = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'Shows_Button.png'))
ButtonTvShowsS = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'Shows_ButtonS.png'))
ButtonSearch = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'button_search.png'))
ButtonSearchS = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'button_searchS.png'))
ButtonQuit = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'Quit_Button.png'))
ButtonQuitS = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'Quit_ButtonS.png'))
List_Focused_default = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'list-bg-selected-default.png'))
List_bg = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'list-bg.png'))
MovieBase = 'https://streamlord.to/'
#############################################################
########## Function To Call That Starts The Window ##########


def MainWindow():
    window = Main('EntertainMe')
    window.doModal()
    del window


def pop(self):
    global logos
    global urls
    global movietitles
    logos = []
    urls = []
    movietitles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    MovieBase = 'https://streamlord.to/'
    Base_Url = 'https://streamlord.to/'
    link = requests.get(MovieBase, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('div', class_={'ml-item'})
    urls.append('')
    movietitles.append('')
    logos.append('')
    liz = xbmcgui.ListItem('[COLOR red][B]Latest Added[/B][/COLOR]')
    liz.setArt({"thumb": Addonicon})
    liz.setPath('null')
    self.LIST.addItem(liz)
    for i in data:
        name = i.a['oldtitle']
        url = i.a['href']
        icon = i.img['src']
        if not Base_Url in url:
            url = ('%s%s' % (Base_Url, url))
        if not Base_Url in icon:
            icon = Base_Url+icon
        movietitles.append(name)
        urls.append(url)
        logos.append(icon)
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb": icon})
        self.LIST.addItem(liz)


def search(self):
    string = ''
    keyboard = xbmc.Keyboard(
        string, '[COLOR yellow][B]What Are We Searching For?[/B][/COLOR]')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        string = string.replace(' ', '+')
        if len(string) > 1:
            dialog.notification(
                AddonTitle, "[COLOR red][B]Searching Now![/B][/COLOR]", Addonicon, 5000)
            term = string.lower()
            url = ('https://streamlord.to/search/%s' % term)
            DisplaySearch(self, url)
        else:
            dialog.notification(
                AddonTitle, "[COLOR red][B]Sorry, No Search Term Was Entered![/B][/COLOR]", Addonicon, 5000)
        quit()


def DisplaySearch(self, url):
    global logos
    global urls
    global movietitles
    self.LIST2.reset()
    logos = []
    urls = []
    movietitles = []
    Base_Url = 'https://streamlord.to'
    self.LIST2.setVisible(True)
    self.button1.controlRight(self.LIST2)
    self.button2.controlRight(self.LIST2)
    self.button4.controlLeft(self.LIST2)
    self.button3.controlLeft(self.LIST2)
    self.LIST.setVisible(False)
    urls.append('')
    movietitles.append('')
    logos.append('')
    liz = xbmcgui.ListItem('[COLOR red][B]Search Results[/B][/COLOR]')
    liz.setArt({"thumb": Addonicon})
    self.LIST2.addItem(liz)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    link = requests.get(url, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('div', class_={'ml-item'})
    for i in data:
        name = i.a['oldtitle']
        url2 = i.a['href']
        icon = i.img['src']
        if not Base_Url in url2:
            url2 = ('%s%s' % (Base_Url, url2))
        if not Base_Url in icon:
            icon = Base_Url+icon
        movietitles.append(name)
        urls.append(url2)
        logos.append(icon)
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb": icon})
        self.LIST2.addItem(liz)
    try:
        NextPageUrl = url.split('page=')[-1]
        oldurl = url.rsplit('page=', 1)[0]
        NewNextPageUrl = int(NextPageUrl) + 1
        NextPageUrl = ('%spage=%s' % (oldurl, NewNextPageUrl))
        name = 'Next Page'
        movietitles.append(name)
        urls.append('NEXT:::%s' % NextPageUrl)
        logos.append(Addonicon)
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb": Addonicon})
        self.LIST2.addItem(liz)
    except:
        pass
    self.setFocus(self.LIST2)


def GetSeasons(self, Media_Url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    link = requests.get(Media_Url, headers=headers, timeout=15).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find('div', class_={'row'})
    streamname = []
    streamurl = []
    for i in data.find_all('li'):
        name = i.text
        url2 = Media_Url
        # if not MovieBase in url2: url2 = ('%s%s' % (MovieBase,url2))
        streamname.append(name)
        streamurl.append(url2)
    select = dialog.select('Choose a Season', streamname)
    if select < 0:
        quit()
    else:
        GetEpisodes(self, streamname[select], streamurl[select])


def GetEpisodes(self, Season, Media_Url):
    season = Season.lower().replace(' ', '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    link = requests.get(Media_Url, headers=headers, timeout=15).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find('div', id={season})
    streamname = []
    streamurl = []
    for i in data.find_all('a'):
        name = i.text
        ids = i['id']
        streamname.append(name)
        streamurl.append(ids)
    select = dialog.select('Choose An Episode', streamname)
    if select < 0:
        quit()
    PLAYTV(Media_Title, streamurl[select], Media_Icon)


def FINDLINKS(self, Media_Url):
    if 'NEXT:::' in Media_Url:
        Media_Url = Media_Url.replace('NEXT:::', '')
        if 'series?' in Media_Url:
            TVSHOWS(self, Media_Url)
            quit()
        else:
            MOVIES(self, Media_Url)
            quit()
    if '/tvshow/' in Media_Url:
        GetSeasons(self, Media_Url)
        quit()
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        sourceurl = 'https://streamlord.to/embed/get?action=movie_embed&mid=%s&l=1'
        link = requests.get(Media_Url, headers=headers).text
        soup = BeautifulSoup(link, 'html.parser')
        mid = soup.find('input', class_={'rating rating-loading'})['movie-id']
        link2 = requests.get(sourceurl % mid, headers=headers).json()
        media = link2['server2']
        link3 = requests.get(media, headers=headers).text
        m3u8pat = r'''['"]([^'"]+m3u8.*?)['"]'''
        getsource = re.findall(m3u8pat, link3)[0]
        PLAY(Media_Title, getsource, Media_Icon)


def PLAY(name, url, iconmedia):
    url = url + \
        '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    dialog.notification(
        AddonTitle, '[COLOR red]Trying To Resolve Link Now[/COLOR]', iconmedia, 2500)
    liz = xbmcgui.ListItem(name)
    liz.setArt({"thumb": iconmedia})
    liz.setPath(url)
    xbmc.Player().play(url, liz, False)


def PLAYTV(name, url, iconmedia):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    sourceurl = 'https://streamlord.to/embed/get?action=episode_embed&eid=%s&l=10'
    link2 = requests.get(sourceurl % url, headers=headers).json()
    try:
        media = link2['server_1']
    except:
        media = link2['server_2']
    link3 = requests.get(media, headers=headers).text
    m3u8pat = r'''['"]([^'"]+m3u8.*?)['"]'''
    getsource = re.findall(m3u8pat, link3)[0]
    getsource = getsource + \
        '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    PLAY(Media_Title, getsource, Media_Icon)


def TVSHOWS(self, url):
    global logos
    global urls
    global movietitles
    self.LIST2.reset()
    logos = []
    urls = []
    movietitles = []
    Base_Url = 'https://streamlord.to'
    self.LIST2.setVisible(True)
    self.button1.controlRight(self.LIST2)
    self.button2.controlRight(self.LIST2)
    self.button4.controlLeft(self.LIST2)
    self.button3.controlLeft(self.LIST2)
    self.LIST.setVisible(False)
    urls.append('')
    movietitles.append('')
    logos.append('')
    liz = xbmcgui.ListItem('[COLOR red][B]TV SHOWS[/B][/COLOR]')
    liz.setArt({"thumb": Addonicon})
    self.LIST2.addItem(liz)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    link = requests.get(url, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('div', class_={'ml-item'})
    for i in data:
        name = i.a['oldtitle']
        url2 = i.a['href']
        icon = i.img['src']
        if not Base_Url in url2:
            url2 = ('%s%s' % (Base_Url, url2))
        if not Base_Url in icon:
            icon = Base_Url+icon
        movietitles.append(name)
        urls.append(url2)
        logos.append(icon)
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb": icon})
        self.LIST2.addItem(liz)
    try:
        NextPageUrl = url.split('page=')[-1]
        oldurl = url.rsplit('page=', 1)[0]
        NewNextPageUrl = int(NextPageUrl) + 1
        NextPageUrl = ('%spage=%s' % (oldurl, NewNextPageUrl))
        name = 'Next Page'
        movietitles.append(name)
        urls.append('NEXT:::%s' % NextPageUrl)
        logos.append(Addonicon)
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb": Addonicon})
        self.LIST2.addItem(liz)
    except:
        pass
    self.setFocus(self.LIST2)


def MOVIES(self, url):
    global logos
    global urls
    global movietitles
    self.LIST2.reset()
    logos = []
    urls = []
    movietitles = []
    Base_Url = 'https://streamlord.to'
    self.LIST2.setVisible(True)
    self.button1.controlRight(self.LIST2)
    self.button2.controlRight(self.LIST2)
    self.button4.controlLeft(self.LIST2)
    self.button3.controlLeft(self.LIST2)
    self.LIST.setVisible(False)
    urls.append('')
    movietitles.append('')
    logos.append('')
    liz = xbmcgui.ListItem('[COLOR red][B]Movies[/B][/COLOR]')
    liz.setArt({"thumb": Addonicon})
    self.LIST2.addItem(liz)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    link = requests.get(url, headers=headers).text
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('div', class_={'ml-item'})
    for i in data:
        name = i.a['oldtitle']
        url2 = i.a['href']
        icon = i.img['src']
        if not Base_Url in url2:
            url2 = ('%s%s' % (Base_Url, url2))
        if not Base_Url in icon:
            icon = Base_Url+icon
        movietitles.append(name)
        urls.append(url2)
        logos.append(icon)
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb": icon})
        self.LIST2.addItem(liz)
    try:
        NextPageUrl = url.split('page=')[-1]
        oldurl = url.rsplit('page=', 1)[0]
        NewNextPageUrl = int(NextPageUrl) + 1
        NextPageUrl = ('%spage=%s' % (oldurl, NewNextPageUrl))
        name = 'Next Page'
        movietitles.append(name)
        urls.append('NEXT:::%s' % NextPageUrl)
        logos.append(Addonicon)
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb": Addonicon})
        self.LIST2.addItem(liz)
    except:
        pass
    self.setFocus(self.LIST2)


def Genre(self, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    caturl = []
    catname = []
    try:
        link = requests.get(url, headers=headers, timeout=15).text
    except:
        dialog.notification(
            AddonTitle, "[COLOR red][B]Source is Slow, Try Again Please![/B][/COLOR]", Addonicon, 5000)
        quit()
    soup = BeautifulSoup(link, 'html.parser')
    data = soup.find_all('ul', class_={'sub-menu'})[1]
    for i in data.find_all('li'):
        try:
            name = i.a.text
            url2 = i.a['href']
            # if not MovieBase in url2: url2 = MovieBase+url2
            catname.append(name)
            caturl.append(url2)
        except:
            pass
    select = dialog.select('Choose A Category', catname)
    if select < 0:
        quit()
    MOVIES(self, caturl[select], catname[select])


def killaddon(self):
    xbmc.executebuiltin("Container.Update(path,replace)")
    xbmc.executebuiltin("ActivateWindow(Home)")

#############################################################
######### Class Containing the GUi Code / Controls ##########


class Main(pyxbmct.AddonFullWindow):
    xbmc.executebuiltin("Dialog.Close(busydialog)")

    def __init__(self, title='EntertainMe'):
        super(Main, self).__init__(title)
        # self.setFocus(self.button6)
        self.setGeometry(1280, 720, 100, 50)
        Background = pyxbmct.Image(Background_Image)
        SearchText = pyxbmct.Image(SText)
        self.placeControl(Background, -10, -1, 123, 52)
        self.placeControl(SearchText, 58, 38, 10, 8)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, lambda: killaddon(self))
        self.connect(self.LIST, lambda: FINDLINKS(self, Media_Url))
        self.connect(self.LIST2, lambda: FINDLINKS(self, Media_Url))
        self.connect(self.button2, lambda: TVSHOWS(
            self, 'https://streamlord.to/series?page=1'))
        self.connect(self.button3, lambda: search(self))
        self.connect(self.button1, lambda: MOVIES(
            self, 'https://streamlord.to/movies?page=1'))
        self.connect(self.button4, lambda: killaddon(self))
        pop(self)
        self.setFocus(self.LIST)
        self.LIST2.setVisible(False)

    def set_info_controls(self):
        self.Hello = pyxbmct.Label(
            '', textColor='0xFFF44248', font='font60', alignment=pyxbmct.ALIGN_CENTER)
        # self.DATE =  pyxbmct.Label('',textColor='0xFFFFFF00', font='font18')
        self.placeControl(self.Hello, -4, 1, 1, 50)
        # self.placeControl(self.DATE,  -9, 20\, 12, 15)

    def set_active_controls(self):
        self.LIST = pyxbmct.List(buttonFocusTexture=List_Focused_default, buttonTexture=None, _imageWidth=80,
                                 _imageHeight=80, _space=0, _itemHeight=54,  _itemTextXOffset=20, _itemTextYOffset=-4, textColor='0xFFFFFFFF')
        self.placeControl(self.LIST, 21, 13, 97, 24)
        self.LIST2 = pyxbmct.List(buttonFocusTexture=List_Focused_default, buttonTexture=None, _imageWidth=80,
                                  _imageHeight=80, _space=0, _itemHeight=54,  _itemTextXOffset=20, _itemTextYOffset=-4, textColor='0xFFFFFFFF')
        self.placeControl(self.LIST2, 21, 13, 97, 24)
        self.button1 = pyxbmct.Button(
            '',   focusTexture=ButtonMoviesS,   noFocusTexture=ButtonMovies)
        self.placeControl(self.button1, 80, 3,  22, 8)
        self.button2 = pyxbmct.Button(
            '',   focusTexture=ButtonTvShowsS,   noFocusTexture=ButtonTvShows)
        self.placeControl(self.button2, 95, 3,  22, 8)
        self.button3 = pyxbmct.Button(
            '',   focusTexture=ButtonSearchS,   noFocusTexture=ButtonSearch)
        self.placeControl(self.button3, 80, 39,  22, 8)
        self.button4 = pyxbmct.Button(
            '',   focusTexture=ButtonQuitS,   noFocusTexture=ButtonQuit)
        self.placeControl(self.button4, 95, 39,  22, 8)

        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.list_update)

    def set_navigation(self):
        self.LIST.controlLeft(self.button1)
        self.LIST2.controlLeft(self.button1)
        self.button4.controlLeft(self.LIST)
        self.button3.controlLeft(self.LIST)

        self.LIST.controlRight(self.button3)
        self.LIST2.controlRight(self.button3)
        self.button1.controlRight(self.LIST)
        self.button2.controlRight(self.LIST)

        self.button1.controlDown(self.button2)
        self.button3.controlDown(self.button4)

        self.button2.controlUp(self.button1)
        self.button4.controlUp(self.button3)

    def list_update(self):
        global Media_Url
        global Media_Title
        global Media_Icon
        if self.getFocus() == self.LIST:
            Position = self.LIST.getSelectedPosition()
            Media_Url = urls[Position]
            Media_Title = movietitles[Position]
            Media_Icon = logos[Position]
        elif self.getFocus() == self.LIST2:
            Position = self.LIST2.getSelectedPosition()
            Media_Url = urls[Position]
            Media_Title = movietitles[Position]
            Media_Icon = logos[Position]

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=rotate start=0 end=720 time=1',),
                               ('WindowClose', 'effect=slide start=100 end=1400 time=500',)])
