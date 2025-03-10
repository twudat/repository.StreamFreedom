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
import random
from datetime import datetime
import re
import Video
import string
import Data
import glob
import base64
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup

addon_id = 'plugin.video.sportie'
selfAddon = xbmcaddon.Addon(id=addon_id)

Paired = 0
PinNeeded = 1
defevent = 'usasports'


####################################################################
########################### CUSTOM OPTIONS###########################
_addon_id_ = 'plugin.video.sportie'
AddonTitle = ('[COLOR aqua][B]S[COLOR red]PORTI[COLOR aqua]E[/B][/COLOR]')
####################################################################
_self_ = xbmcaddon.Addon(id=_addon_id_)
_images_ = '/resources/artwork/'
log_file = xbmcvfs.translatePath(os.path.join('special://home/kodi.log'))
dialog = xbmcgui.Dialog()
Date = time.strftime("%d/%m")
####################################################################
# MAIN IMAGES
####################################################################
Skin_Path = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_))
Background_Image = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'MainbgNew3.png'))
User_ID_Font = xbmcvfs.translatePath(os.path.join(Skin_Path, 'C800.ttf'))
Background_Report = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'MainbgREPORT3.png'))
Background_Pair = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'PairingBG1.png'))
Background_Prem = xbmcvfs.translatePath(os.path.join(Skin_Path, 'PremBG1.png'))
Background_Replays = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'ReplaysBG.png'))
AddonIcon = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'Icon.png'))
Addon_V_File = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'addon.xml'))
temp_image_save = xbmcvfs.translatePath(os.path.join(
    'special://home/userdata/addon_data/' + _addon_id_, '%s.png'))
delete_temp = xbmcvfs.translatePath(os.path.join(
    'special://home/userdata/addon_data/' + _addon_id_))

####################################################################
# PREM BUTTON IMAGES
####################################################################

UKFootieNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'FootballButtonNS.png'))
UKFootieS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'FootballButtonS.png'))

LivePPVNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'PPVButtonNS.png'))
LivePPVS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'PPVButtonS.png'))

PremSportsNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'USButtonNS.png'))
PremSportsS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'USButtonS.png'))

IntSportsNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'UKButtonNS.png'))
IntSportsS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'UKButtonS.png'))

SportsNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'USEVENTSNS.png'))
SportsS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'USEVENTSS.png'))

####################################################################
# Replays BUTTON IMAGES
####################################################################

NFLNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'NFLButtonNS.png'))
NFLS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'NFLButtonS.png'))

NBANS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'NBAButtonNS.png'))
NBAS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'NBAButtonS.png'))

FOOTIENS = xbmcvfs.translatePath(os.path.join(
    Skin_Path, 'REPLAYFOOTBALLButtonNS.png'))
FOOTIES = xbmcvfs.translatePath(os.path.join(
    Skin_Path, 'REPLAYFOOTBALLButtonS.png'))


####################################################################
# Intro Video
####################################################################
intro_video = xbmcvfs.translatePath(os.path.join(Skin_Path, 'intro.mp4'))


####################################################################
# BUTTON IMAGES
####################################################################
FootieNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'footiebutton3NS.png'))
FootieS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'footiebutton3S.png'))

MotorSportsNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'motorsports2NS.png'))
MotorSportsS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'motorsports2S.png'))

OtherSportsNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'otherbutton2NS.png'))
OtherSportsS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'otherbutton2S.png'))

requestNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'requestBUTTONNS.png'))
requestS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'requestBUTTONS.png'))

replaysNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'replaysBUTTONNS.png'))
replaysS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'replaysBUTTONS.png'))

errorNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'errorBUTTONNS.png'))
errorS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'errorBUTTONS.png'))

QuitNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'quitBUTTONNS.png'))
QuitS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'quitBUTTONS.png'))

MainMenuNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'mainmenuBUTTONNS.png'))
MainMenuS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'mainmenuBUTTONS.png'))

PairButtonNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'PAIREDNS.png'))
PairButtonS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'PAIREDS.png'))

PairButtonQuitNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'PAIREDQUITNS.png'))
PairButtonQuitS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'PAIREDQUITS.png'))

PremiumNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'premiumbuttonNS.png'))
PremiumS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'premiumbuttonS.png'))

####################################################################
# OTHER IMAGES
####################################################################
List_Focused = xbmcvfs.translatePath(os.path.join(Skin_Path, 'ListBGF.png'))
List_NFocused = xbmcvfs.translatePath(os.path.join(Skin_Path, 'ListBG.png'))

####################################################################
# API URLS
####################################################################
api_url_events = 'https://sportie.app/Apis/api.json'
api_sportie = 'https://nemzzyprivate.com/sportieapi.php'
error_api = 'https://nemzzyprivate.com/reportissue.php'
pair_api = 'https://sportie.app/service.php'

user_agent_list = [
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
     "Chrome/77.0.3865.90 Safari/537.36"),
    ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
     "Chrome/79.0.3945.130 Safari/537.36"),
    ("Mozilla/5.0 (Linux; Android 14; SM-M136B Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko)"
     "Version/4.0 Chrome/130.0.6723.106 Mobile Safari/537.36 WebView MetaMaskMobile"),
    ("Mozilla/5.0 (iPad; CPU OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
     "CriOS/128.0.6613.92 Mobile/15E148 Safari/604.1")
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
        "Referer": "https://ppv.land/"
    }
    return headers


def MainWindow():

    window = Main('sportie')
    window.doModal()
    del window


def Get_Version(self):
    pattern = r'''<addon id.*?version="(.*?)"'''
    with open(Addon_V_File, 'r') as file:
        contents = file.read()
        get_v = re.findall(pattern, contents)[0]
        dialog.notification(
            AddonTitle, '[COLOR aqua]Sportie Version : %s[/COLOR]' % get_v, AddonIcon, 6000)


def send_report(problem):
    if problem == 1:
        pass
    elif problem == 2:
        issue_to_report = 'Issue : Motorsport catergory is empty'
    elif problem == 3:
        issue_to_report = 'Issue : Football catergory is empty'
    elif problem == 4:
        issue_to_report = 'Issue : Other catergory is empty'
    elif problem == 5:
        issue_to_report = 'Issue : Event missing from scheduel'
        dialog.ok(AddonTitle, "[COLOR aqua]Sometime events appear on the scheduel on the day or a few hours before they start, if you think we have missed an event please use the request button[/COLOR]")
    else:
        issue_to_report = 'Issue : Other issue reported'
    if problem != 5:
        with open(log_file, 'rb') as file:
            files = {'file': file}
            data = {'error': issue_to_report}
            response = requests.post(error_api, data=data, files=files)
        dialog.ok(AddonTitle, "[COLOR red]%s[/COLOR]" % response.text)


def Replays(self, event):
    global replayurl
    global replayname
    global replayevent
    replayurl = []
    replayname = []
    replayevent = []
    replayevent = event
    self.LISTReplay.reset()
    from scrapers import sources
    _sources = sources()
    for indexer in _sources:
        try:
            getcontent = indexer[1].Get_Events(event)
            for info in getcontent:
                replayname.append(info['title'])
                replayurl.append(info['url'])
                self.LISTReplay.addItem(info['title'])
        except Exception:
            pass


def Replay_Resolver(self, event, replaytitle, replayurl):
    if 'football' in event:
        Replay_Resolver_Football(self, event, replaytitle, replayurl)
        quit()
    from scrapers import sources
    _sources = sources()
    found = 0
    dialog.notification(
        AddonTitle, '[COLOR aqua]Hunting Links Now[/COLOR]', AddonIcon, 2500)
    for indexer in _sources:
        getmedia = indexer[1].Resolve_link(event, replayurl)
        if getmedia:
            streamurl = []
            streamname = []
            for info in getmedia:
                found += 1
                title = ("Link %s" % found)
                streamname.append(title)
                streamurl.append(info['url'])
            select = dialog.select(replaytitle, streamname)
            if select < 0:
                quit()
            stream_url = streamurl[select]
            liz = xbmcgui.ListItem(replaytitle)
            liz.setProperty('IsPlayable', 'true')
            liz.setPath(stream_url)
            self.close()
            xbmc.Player().play(stream_url, liz, False)


def Replay_Resolver_Football(self, event, replaytitle, replayurl):
    from scrapers import sources
    _sources = sources()
    found = 0
    dialog.notification(
        AddonTitle, '[COLOR aqua]Hunting Links Now[/COLOR]', AddonIcon, 2500)
    for indexer in _sources:
        getmedia = indexer[1].Resolve_link(event, replayurl)
        if getmedia:
            streamurl = []
            streamname = []
            for info in getmedia:
                found += 1
                title = ("Link %s" % found)
                streamname.append(info['title'])
                streamurl.append(info['url'])
            select = dialog.select(replaytitle, streamname)
            if select < 0:
                quit()
            stream_url = streamurl[select]
            liz = xbmcgui.ListItem(replaytitle)
            liz.setProperty('IsPlayable', 'true')
            liz.setPath(stream_url)
            self.close()
            xbmc.Player().play(stream_url, liz, False)


def Check_pair(self):
    if PinNeeded == 1:
        global Paired
        global get_id
        global expiry_time
        data = {'code': get_id}
        check = requests.post(pair_api, data=data).json()
        get_status = check['results']['Status']
        if get_status == 'Valid':
            Paired = 1
            expiry_time = check['results']['Expires']

        else:
            Paired = 0
            selfAddon.setSetting('user_id', '')
            get_id = Data.make_userid()
            Pair_Addon()
    else:
        Paired = 1
        expiry_time = 1768842189


def Check_code(self):
    global Paired
    global get_id
    global expiry_time
    data = {'code': get_id}
    check = requests.post(pair_api, data=data).json()
    get_status = check['results']['Status']
    if get_status == 'Valid':
        Paired = 1
        expiry_time = check['results']['Expires']
        self.close()
    elif get_status == 'Invalid':
        Paired = 0
        dialog.notification(
            AddonTitle, '[COLOR aqua]Sorry This Code Hasn\'t Been Paired Yet[/COLOR]', AddonIcon, 6000)
    else:
        Paired = 0
        dialog.notification(
            AddonTitle, '[COLOR aqua]Sorry The Code Is Expired, Generating a new code[/COLOR]', AddonIcon, 6000)
        for filename in os.listdir(delete_temp):
            if filename.endswith('.png'):
                os.remove(os.path.join(delete_temp, filename))
                selfAddon.setSetting('user_id', '')
                get_id = Data.make_userid()
                self.close()
                Pair_Addon()


def Get_Prem_Streams(self, event):
    global defevent
    defevent = event
    prem_url = 'http://moontv.life/enigma2.php?username=sportieaddon&password=sportieaddon&type=get_live_streams&cat_id=%s'
    global Item_Title
    global Item_Link
    self.LISTPrem.reset()
    Item_Title = []
    Item_Link = []
    self.LISTPrem.addItem(event.title())
    Item_Title.append('')
    Item_Link.append('')
    if 'sportsgroup' in event:
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle, "Getting Sports Events")
        us_sports_group = [47, 108, 8, 10, 7, 9, 59]
        for ids in us_sports_group:
            if ids == 47:
                progress = 15
                dp_title = 'NCAFF'
            elif ids == 108:
                progress = 30
                dp_title = 'NCAAB(College Basketball)'
            elif ids == 8:
                progress = 45
                dp_title = 'NFL)'
            elif ids == 10:
                progress = 60
                dp_title = 'NBA'
            elif ids == 7:
                progress = 75
                dp_title = 'MLB'
            elif ids == 9:
                progress = 90
                dp_title = 'NHL'
            elif ids == 59:
                progress = 100
                dp_title = 'MLS'
            link = requests.get(prem_url % ids).text
            soup = BeautifulSoup(link, 'html.parser')
            r = soup.find_all('channel')
            for i in r:
                title = base64.b64decode(i.find('title').text).decode()
                url = i.find('stream_url').text
                Item_Title.append(title)
                Item_Link.append(url+'|User-Agent=sportie')
                self.LISTPrem.addItem('[B]%s[/B]' % title)
                dp.update(progress, "Getting Events from %s" % dp_title)
        dp.close()
        open_id = 4
    elif 'ppv' in event:
        open_id = 12
    elif 'ukfootie' in event:
        open_id = 55
    elif 'intsports' in event:
        open_id = 38
    elif 'usasports' in event:
        open_id = 4
    link = requests.get(prem_url % open_id).text
    soup = BeautifulSoup(link, 'html.parser')
    r = soup.find_all('channel')
    for i in r:
        title = base64.b64decode(i.find('title').text).decode()
        url = i.find('stream_url').text
        Item_Title.append(title)
        Item_Link.append(url+'?Connection=keep-alive|User-Agent=sportie')
        self.LISTPrem.addItem('[B]%s[/B]' % title)


def Player(self, name, url):

    stream_url = url
    liz = xbmcgui.ListItem(name)
    liz.setProperty('IsPlayable', 'true')
    liz.setPath(stream_url)
    self.close()
    xbmc.Player().play(stream_url, liz, False)
    while (xbmc.getCondVisibility("Player.HasMedia")):
        time.sleep(2)
        pass
    else:
        Prem_Streams()


def Prem_Streams():
    # PREM WINDOW
    class Prem_Streams(pyxbmct.BlankDialogWindow):
        def __init__(self):
            # T L H W
            super(Prem_Streams, self).__init__()
            self.setGeometry(1000, 600, 100, 100)
            self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
            self.set_active_controls()
            self.set_navigation()
            self.setFocus(self.Uk_Footie)
            self.connect(self.Uk_Footie,
                         lambda: Get_Prem_Streams(self, 'ukfootie'))
            self.connect(self.All, lambda: Get_Prem_Streams(
                self, 'sportsgroup'))
            self.connect(self.PPV, lambda: Get_Prem_Streams(self, 'ppv'))
            self.connect(self.Int, lambda: Get_Prem_Streams(self, 'intsports'))
            self.connect(
                self.Prem, lambda: Get_Prem_Streams(self, 'usasports'))
            self.connect(self.LISTPrem, lambda: Player(
                self, str(Media_Title), str(Media_Link)))
            Get_Prem_Streams(self, defevent)

        def set_active_controls(self):
            window_bg = pyxbmct.Image(Background_Prem)
            self.placeControl(window_bg, 0, 0, rowspan=100, columnspan=100)

            self.Uk_Footie = pyxbmct.Button(
                '',   focusTexture=UKFootieS,   noFocusTexture=UKFootieNS)
            self.placeControl(self.Uk_Footie, 15, 2, 15, 30)

            self.PPV = pyxbmct.Button(
                '',   focusTexture=LivePPVS,   noFocusTexture=LivePPVNS)
            self.placeControl(self.PPV, 31, 2, 15, 30)

            self.Prem = pyxbmct.Button(
                '',   focusTexture=PremSportsS,   noFocusTexture=PremSportsNS)
            self.placeControl(self.Prem, 47, 2, 15, 30)

            self.Int = pyxbmct.Button(
                '',   focusTexture=IntSportsS,   noFocusTexture=IntSportsNS)
            self.placeControl(self.Int, 63, 2, 15, 30)

            self.All = pyxbmct.Button(
                '',   focusTexture=SportsS,   noFocusTexture=SportsNS)
            self.placeControl(self.All, 79, 2, 15, 30)

            self.LISTPrem = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture=List_NFocused, _imageWidth=1,
                                         _imageHeight=2, _space=2, _itemHeight=50,  _itemTextXOffset=6, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
            self.placeControl(self.LISTPrem, 16, 35, 84, 62)

            self.connectEventList(
                [pyxbmct.ACTION_MOVE_DOWN,
                 pyxbmct.ACTION_MOVE_UP,
                 pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
                 pyxbmct.ACTION_MOUSE_WHEEL_UP,
                 pyxbmct.ACTION_MOUSE_MOVE],
                self.list_update)

        def set_navigation(self):
            # DOWN
            self.Uk_Footie.controlDown(self.PPV)
            self.PPV.controlDown(self.Prem)
            self.Prem.controlDown(self.Int)
            self.Int.controlDown(self.All)
            # UP
            self.PPV.controlUp(self.Uk_Footie)
            self.Prem.controlUp(self.PPV)
            self.Int.controlUp(self.Prem)
            self.All.controlUp(self.Int)
            # RIGHT
            self.Uk_Footie.controlRight(self.LISTPrem)
            self.PPV.controlRight(self.LISTPrem)
            self.Prem.controlRight(self.LISTPrem)
            self.Int.controlRight(self.LISTPrem)
            self.All.controlRight(self.LISTPrem)
            # LEFT
            self.LISTPrem.controlLeft(self.Uk_Footie)

        def list_update(self):
            global Media_Title
            global Media_Link
            global Media_Desc
            global Media_Icon
            try:
                if self.getFocus() == self.LISTPrem:
                    position = self.LISTPrem.getSelectedPosition()
                    Media_Title = Item_Title[position]
                    Media_Link = Item_Link[position]
            except (RuntimeError, SystemError):
                pass
    windowPrem = Prem_Streams()
    windowPrem.doModal()
    del windowPrem


def Replays_Window():
    # PREM WINDOW
    class Replays_Window(pyxbmct.BlankDialogWindow):
        def __init__(self):
            # T L H W
            super(Replays_Window, self).__init__()
            self.setGeometry(1000, 600, 100, 100)
            self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
            self.set_active_controls()
            self.set_navigation()
            self.connect(self.NFL, lambda: Replays(self, 'nfl'))
            self.connect(self.NBA, lambda: Replays(self, 'nba'))
            self.connect(self.FOOTIE, lambda: Replays(self, 'football'))
            self.connect(self.LISTReplay, lambda: Replay_Resolver(
                self, replayevent, str(Media_Title), str(Media_Link)))
            self.setFocus(self.NFL)

        def set_active_controls(self):
            window_bg = pyxbmct.Image(Background_Replays)
            self.placeControl(window_bg, 0, 0, rowspan=100, columnspan=100)

            self.NFL = pyxbmct.Button(
                '',   focusTexture=NFLS,   noFocusTexture=NFLNS)
            self.placeControl(self.NFL, 20, 2, 15, 30)

            self.NBA = pyxbmct.Button(
                '',   focusTexture=NBAS,   noFocusTexture=NBANS)
            self.placeControl(self.NBA, 36, 2, 15, 30)

            self.FOOTIE = pyxbmct.Button(
                '',   focusTexture=FOOTIES,   noFocusTexture=FOOTIENS)
            self.placeControl(self.FOOTIE, 52, 2, 15, 30)

            self.LISTReplay = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture=List_NFocused, _imageWidth=1,
                                           _imageHeight=2, _space=2, _itemHeight=50,  _itemTextXOffset=6, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
            self.placeControl(self.LISTReplay, 16, 35, 84, 62)

            self.connectEventList(
                [pyxbmct.ACTION_MOVE_DOWN,
                 pyxbmct.ACTION_MOVE_UP,
                 pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
                 pyxbmct.ACTION_MOUSE_WHEEL_UP,
                 pyxbmct.ACTION_MOUSE_MOVE],
                self.list_update)

        def set_navigation(self):
            # down
            self.NFL.controlDown(self.NBA)
            self.NBA.controlDown(self.FOOTIE)
            # up
            self.FOOTIE.controlUp(self.NBA)
            self.NBA.controlUp(self.NFL)
            # right
            self.FOOTIE.controlRight(self.LISTReplay)
            self.NBA.controlRight(self.LISTReplay)
            self.NFL.controlRight(self.LISTReplay)
            # left
            self.LISTReplay.controlLeft(self.NFL)

        def list_update(self):
            global Media_Title
            global Media_Link
            try:
                if self.getFocus() == self.LISTReplay:
                    position = self.LISTReplay.getSelectedPosition()
                    Media_Title = replayname[position]
                    Media_Link = replayurl[position]
            except (RuntimeError, SystemError):
                pass
    windowReplays = Replays_Window()
    windowReplays.doModal()
    del windowReplays


def Report_Issue():
    # ISSUE WINDOW
    class Report_Issue(pyxbmct.BlankDialogWindow):
        def __init__(self):
            # T L H W
            super(Report_Issue, self).__init__()
            self.setGeometry(600, 600, 100, 100)
            self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
            self.set_active_controls()
            self.connect(self.LIST, lambda: send_report(Issue))
            self.connect(self.MainMenu_button, self.close)
            self.setFocus(self.LIST)
            self.set_navigation()

        def set_active_controls(self):
            global issues
            issues = []
            image = pyxbmct.Image(Background_Report)
            self.placeControl(image, 0, 0, rowspan=100, columnspan=100)
            self.MainMenu_button = pyxbmct.Button(
                '',   focusTexture=MainMenuS,   noFocusTexture=MainMenuNS)
            self.placeControl(self.MainMenu_button, 78, 40, 20, 20)
            self.LIST = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture=List_NFocused, _imageWidth=1,
                                     _imageHeight=2, _space=2, _itemHeight=50,  _itemTextXOffset=6, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
            self.placeControl(self.LIST, 16, 4, 60, 90)
            self.LIST.addItem(
                "[COLOR aqua]Select issue from the list below[/COLOR]")
            issues.append(1)
            self.LIST.addItem("Motorsport catergory not working or empty")
            issues.append(2)
            self.LIST.addItem("Football catergory not working or empty")
            issues.append(3)
            self.LIST.addItem("Other catergory not working or empty")
            issues.append(4)
            self.LIST.addItem("Event missing from scheduel")
            issues.append(5)
            self.LIST.addItem("Other error not stated above")
            issues.append(6)
            self.connectEventList(
                [pyxbmct.ACTION_MOVE_DOWN,
                 pyxbmct.ACTION_MOVE_UP,
                 pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
                 pyxbmct.ACTION_MOUSE_WHEEL_UP,
                 pyxbmct.ACTION_MOUSE_MOVE],
                self.list_update)

        def set_navigation(self):
            self.LIST.controlDown(self.MainMenu_button)
            self.MainMenu_button.controlUp(self.LIST)

        def list_update(self):
            global Issue
            try:
                if self.getFocus() == self.LIST:
                    position = self.LIST.getSelectedPosition()
                    Issue = issues[position]
            except (RuntimeError, SystemError):
                pass
    windowUser = Report_Issue()
    windowUser.doModal()
    del windowUser


def Pair_Addon():
    # ISSUE WINDOW
    class Pair_Addon(pyxbmct.BlankDialogWindow):
        def __init__(self):
            # T L H W
            super(Pair_Addon, self).__init__()
            self.setGeometry(800, 600, 100, 100)
            self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
            self.set_active_controls()
            self.connect(self.Pair_button, lambda: Check_code(self))
            self.connect(self.Quit_button, lambda: Kill_No_Pair(self))
            self.Instructions = pyxbmct.Label(
                'PAIRING LASTS 24 HOURS', textColor='0xFFFFFFFF', font='font14')
            self.placeControl(self.Instructions, 54, 34, 12, 40)
            self.setFocus(self.Pair_button)
            self.set_navigation()

            def text_to_png(text, font_path, font_size, output_path):
                # Create a font object
                font = ImageFont.truetype(font_path, font_size)

                # Calculate the size of the text
                text_width, text_height = font.getsize(text)

                # Create a new image with a white background
                image = Image.new('RGB', (text_width, text_height), 'white')

                # Create a drawing context
                draw = ImageDraw.Draw(image)

                # Draw the text onto the image
                draw.text((0, 0), text, font=font, fill='red')

                # Save the image
                image.save(output_path)
            text = get_id
            font_path = User_ID_Font  # Update this path to your font file
            font_size = 120
            output_path = (temp_image_save % text)
            text_to_png(text, font_path, font_size, output_path)
            self.User_ID = pyxbmct.Image(temp_image_save % get_id)
            self.placeControl(self.User_ID, 28, 30, 20, 40)

        def set_active_controls(self):
            image = pyxbmct.Image(Background_Pair)
            self.placeControl(image, 0, 0, rowspan=100, columnspan=100)
            self.Pair_button = pyxbmct.Button(
                '',   focusTexture=PairButtonS,   noFocusTexture=PairButtonNS)
            self.placeControl(self.Pair_button, 58, 10, 20, 40)
            self.Quit_button = pyxbmct.Button(
                '',   focusTexture=PairButtonQuitS,   noFocusTexture=PairButtonQuitNS)
            self.placeControl(self.Quit_button, 58, 50, 20, 40)

            self.connectEventList(
                [pyxbmct.ACTION_MOVE_DOWN,
                 pyxbmct.ACTION_MOVE_UP,
                 pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
                 pyxbmct.ACTION_MOUSE_WHEEL_UP,
                 pyxbmct.ACTION_MOUSE_MOVE],
                self.list_update)

        def set_navigation(self):
            pass

        def list_update(self):
            pass
    try:
        windowUser.destroy()
        windowUser = Pair_Addon()
        windowUser.doModal()
        del windowUser
    except:
        windowUser = Pair_Addon()
        windowUser.doModal()
        del windowUser


def tick(self):
    timestamp = int(time.time())
    datetime1 = datetime.fromtimestamp(expiry_time)
    datetime2 = datetime.fromtimestamp(timestamp)
    time_difference = datetime1 - datetime2
    hours, remainder = divmod(time_difference.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    expire_string = (f"{int(hours)} hours and {int(minutes)} minutes")
    self.Expiry.setLabel('Pairing Expires In : %s' % expire_string)


def QuitAddon(self):
    dialog.notification(
        AddonTitle, '[COLOR aqua]Thank you for using Sportie[/COLOR]', AddonIcon, 2500)
    for filename in os.listdir(delete_temp):
        if filename.endswith('.png'):
            os.remove(os.path.join(delete_temp, filename))
    time.sleep(2)
    xbmc.executebuiltin("Container.Update(path,replace)")
    xbmc.executebuiltin("ActivateWindow(Home)")
    self.close()


def Kill_No_Pair(self):
    dialog.notification(
        AddonTitle, '[COLOR aqua]Sorry you\'ve chosen not to pair[/COLOR]', AddonIcon, 2500)
    self.close()


def get_events(self):
    try:
        data_dict = []
        link = requests.get(
            api_url_events, headers=get_headers(), timeout=5).json()
        data = link['streams']
        for i in data:
            cat = i['category']
            all_events = i['streams']
            for j in all_events:
                stream_id = j['id']
                stream_name = j['name']
                start_time = j['starts_at']
                end_time = j['ends_at']
                data_dict.append({'cat': cat, 'stream_name': stream_name,
                                 'stream_id': stream_id, 'start': start_time, 'end': end_time})
        sorted_data = sorted(data_dict, key=lambda x: x['start'])
        info_string = ''
        for items in sorted_data:
            event = items['cat']
            if not '24/7' in event:
                event_title = items['stream_name']
                event_id = items['stream_id']
                start_time = items['start']
                end_time = items['end']
                start_time = datetime.utcfromtimestamp(
                    start_time).strftime('%A %d %B - %H:%M')
                end_time = datetime.utcfromtimestamp(
                    end_time).strftime('%A %d %B - %H:%M')
                if 'football' in event.lower():
                    section = 'In Football Section'
                elif 'motorsports' in event.lower():
                    section = 'In Motorsport Section'
                else:
                    section = 'In Other Section'
                info_string = info_string + \
                    ("[COLOR lime]%s[/COLOR] \nStarts: %s\nEnds: %s\n[COLOR yellow]%s[/COLOR]\n\n" %
                     (event_title, start_time, end_time, section))
        self.EventBox.setText(
            "[COLOR aqua]LIVE AND UPCOMING EVENTS[/COLOR]\n\n"+info_string)
    except Exception:
        dialog.ok(AddonTitle, "Addon Under Maintenance, try back soon")
        quit()


def get_message(self):
    link = requests.get(api_sportie).json()
    for data in link:
        try:
            addon_message = data['message']['Message']
            self.ChatBox.setText(addon_message)
        except Exception:
            pass
        try:
            check_version = data['important']['Version']
            pattern = r'''<addon id.*?version="(.*?)"'''
            with open(Addon_V_File, 'r') as file:
                contents = file.read()
                get_v = re.findall(pattern, contents)[0]
                if check_version == get_v:
                    pass
                else:
                    dialog.ok(
                        AddonTitle, "Addon out of date, Please update to continue using")
                    quit()
        except Exception:
            pass


def MoveToCat(self, event):
    Video.MainWindow(event)


class Main(pyxbmct.AddonFullWindow):

    def __init__(self, title='sportie'):
        global get_id
        global PinNeeded
        get_id = Data.make_userid()
        link = requests.get(api_sportie).json()
        for data in link:
            try:
                need_pin = data['important']['Pin']
                if need_pin.lower() == 'no':
                    PinNeeded = 0
                else:
                    PinNeeded = 1
            except Exception:
                pass
        Check_pair(self)
        if Paired == 0:
            QuitAddon(self)
            quit()
        else:
            super(Main, self).__init__(title)
            self.setGeometry(1280, 720, 150, 50)
            self.main_bg_img = Background_Image
            self.main_bg = xbmcgui.ControlImage(
                0, 0, 1280, 720, self.main_bg_img)
            self.main_bg.setImage(Background_Image)
            self.addControl(self.main_bg)
            self.set_info_controls()
            self.set_active_controls()
            self.set_navigation()
            self.connect(pyxbmct.ACTION_NAV_BACK, lambda: QuitAddon(self))

            self.ChatBox = pyxbmct.TextBox()
            self.placeControl(self.ChatBox, 112, 18, 54, 32)
            self.ChatBox.autoScroll(2000, 800, 2000)

            self.EventBox = pyxbmct.TextBox()
            self.placeControl(self.EventBox, -6, 1, 170, 16)
            self.EventBox.autoScroll(1500, 800, 1)
            get_events(self)
            get_message(self)
            Get_Version(self)
            self.setFocus(self.Motorsport_button)
            timestamp = int(time.time())
            datetime1 = datetime.fromtimestamp(expiry_time)
            datetime2 = datetime.fromtimestamp(timestamp)
            time_difference = datetime1 - datetime2
            hours, remainder = divmod(time_difference.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            expire_string = (f"{int(hours)} hours and {int(minutes)} minutes")
            self.Expiry = pyxbmct.Label(
                'Pairing Expires In : %s' % expire_string, textColor='0xFFFFFF00', font='font14')
            self.placeControl(self.Expiry, 15, 23, 12, 40)

    def set_info_controls(self):
        pass

    def Multi_Update(self):
        tick(self)
        self.list_update()
        Data.report_to_api()

    def set_active_controls(self):
        # T L H W
        self.Motorsport_button = pyxbmct.Button(
            '',   focusTexture=MotorSportsS,   noFocusTexture=MotorSportsNS)
        self.placeControl(self.Motorsport_button, 30, 18, 50, 10)

        self.Football_button = pyxbmct.Button(
            '',   focusTexture=FootieS,   noFocusTexture=FootieNS)
        self.placeControl(self.Football_button, 30, 29, 50, 10)

        self.Other_button = pyxbmct.Button(
            '',   focusTexture=OtherSportsS,   noFocusTexture=OtherSportsNS)
        self.placeControl(self.Other_button, 30, 40, 50, 10)

        self.Replays_button = pyxbmct.Button(
            '',   focusTexture=replaysS,   noFocusTexture=replaysNS)
        self.placeControl(self.Replays_button, 80, 19, 30, 5)

        self.Error_button = pyxbmct.Button(
            '',   focusTexture=errorS,   noFocusTexture=errorNS)
        self.placeControl(self.Error_button, 80, 27, 30, 5)

        self.Premium_button = pyxbmct.Button(
            '',   focusTexture=PremiumS,   noFocusTexture=PremiumNS)
        self.placeControl(self.Premium_button, 80, 35, 30, 5)

        self.Quit_button = pyxbmct.Button(
            '',   focusTexture=QuitS,   noFocusTexture=QuitNS)
        self.placeControl(self.Quit_button, 80, 43, 30, 5)

        self.connect(self.Quit_button, lambda: QuitAddon(self))
        self.connect(self.Football_button, lambda: MoveToCat(self, 'football'))
        self.connect(self.Motorsport_button,
                     lambda: MoveToCat(self, 'motorsport'))
        self.connect(self.Other_button, lambda: MoveToCat(self, 'other'))
        self.connect(self.Error_button, lambda: Report_Issue())
        self.connect(self.Replays_button, lambda: Replays_Window())
        self.connect(self.Premium_button, lambda: Prem_Streams())

        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOVE_LEFT,
             pyxbmct.ACTION_MOVE_RIGHT,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.Multi_Update)

    def set_navigation(self):
        # DOWN
        self.Motorsport_button.controlDown(self.Replays_button)
        self.Football_button.controlDown(self.Error_button)
        self.Other_button.controlDown(self.Quit_button)

        # LEFT
        self.Football_button.controlLeft(self.Motorsport_button)
        self.Other_button.controlLeft(self.Football_button)
        self.Quit_button.controlLeft(self.Premium_button)
        self.Error_button.controlLeft(self.Replays_button)
        self.Premium_button.controlLeft(self.Error_button)

        # RIGHT
        self.Motorsport_button.controlRight(self.Football_button)
        self.Football_button.controlRight(self.Other_button)
        self.Replays_button.controlRight(self.Error_button)
        self.Error_button.controlRight(self.Premium_button)
        self.Premium_button.controlRight(self.Quit_button)

        # UP
        self.Quit_button.controlUp(self.Other_button)
        self.Error_button.controlUp(self.Football_button)
        self.Replays_button.controlUp(self.Motorsport_button)
        self.Premium_button.controlUp(self.Football_button)

    def list_update(self):
        pass


if __name__ == '__main__':
    MainWindow()
