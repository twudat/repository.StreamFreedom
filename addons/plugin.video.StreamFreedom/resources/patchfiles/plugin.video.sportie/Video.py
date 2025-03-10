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
import Data
from inputstreamhelper import Helper
####################################################################
########################### CUSTOM OPTIONS###########################
_addon_id_ = 'plugin.video.sportie'
AddonTitle = ('[COLOR aqua][B]S[COLOR red]PORTI[COLOR aqua]E[/B][/COLOR]')
####################################################################
_self_ = xbmcaddon.Addon(id=_addon_id_)
_images_ = '/resources/artwork/'
dialog = xbmcgui.Dialog()
Date = time.strftime("%d/%m")
####################################################################
# MAIN IMAGES
####################################################################
Skin_Path = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_))
Background_Image = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'MainbgLinks.png'))
AddonIcon = xbmcvfs.translatePath(os.path.join(
    'special://home/addons/' + _addon_id_, 'Icon.png'))
Background_Report = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'MainbgREPORT3.png'))

####################################################################
# BUTTON IMAGES
####################################################################

errorNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'errorBUTTONNS.png'))
errorS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'errorBUTTONS.png'))

QuitNS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'mainmenuBUTTONNS.png'))
QuitS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'mainmenuBUTTONS.png'))

PremiumNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'premiumbuttonNS.png'))
PremiumS = xbmcvfs.translatePath(os.path.join(Skin_Path, 'premiumbuttonS.png'))

MainMenuNS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'mainmenuBUTTONNS.png'))
MainMenuS = xbmcvfs.translatePath(
    os.path.join(Skin_Path, 'mainmenuBUTTONS.png'))

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
api_stream_sources = ('https://ppv.land/api/streams/%s')
error_api = 'https://nemzzyprivate.com/reportissue.php'

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


def resolve_stream(stream_name, stream_code):
    link = requests.get('https://sportie.app/Apis/%s' %
                        stream_code, headers=get_headers()).json()
    stream_url = link['data']['m3u8']
    # listitem = xbmcgui.ListItem(path=stream_url, offscreen=True)
    # listitem.setProperty('inputstream', 'inputstream.adaptive')
    # listitem.setProperty('inputstream.adaptive.common_headers', 'headername=encoded_value&User-Agent=%s&Origin=https://ppv.land' % random.choice(user_agent_list))
    # xbmc.Player ().play(stream_url, listitem, False)

    is_helper = Helper("hls")
    if is_helper.check_inputstream():
        play_item = xbmcgui.ListItem(path=stream_url)
        play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        play_item.setProperty('inputstream', 'inputstream.adaptive')
        play_item.setProperty('inputstream.adaptive.common_headers',
                              'headername=encoded_value&User-Agent=%s&Origin=https://ppv.land' % random.choice(user_agent_list))
        xbmc.Player().play(stream_url, play_item, False)


def MainWindow(user_choice):
    global picked
    if user_choice == 'football':
        picked = 'football'
    elif user_choice == 'motorsport':
        picked = 'Motorsports'
    else:
        picked = 'other'
    window = Main('sportie')
    window.doModal()
    del window


def tick(self):
    time2 = time.strftime("[COLOR yellow]%H:%M %p[/COLOR]")
    self.TIME.setLabel(str(time2))


def CloseWindow(self):
    self.close()


def get_events(self):
    global Item_Title
    global Item_Link
    Item_Title = []
    Item_Link = []
    Item_Title.append('Links Found By Sportie')
    Item_Link.append('')
    self.LIST.addItem(AddonTitle+' Links')
    live_now = int(time.time())
    data_dict = []
    link = requests.get(api_url_events, headers=get_headers()).json()
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
            start_unix = items['start']
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
            # info_string = info_string + ("[COLOR lime]%s[/COLOR] \nStarts: %s\nEnds: %s\n[COLOR yellow]%s[/COLOR]\n\n" % (event_title,start_time,end_time,section))
            if picked in event.lower():
                info_string = info_string + \
                    ("[COLOR lime]%s[/COLOR] \nStarts: %s\nEnds: %s\n\n" %
                     (event_title, start_time, end_time))
                if live_now >= start_unix:
                    self.LIST.addItem(event_title + '| ' +
                                      '[COLOR lime]LIVE NOW[/COLOR]')
                    Item_Title.append(event_title+'|'+str(start_unix))
                    Item_Link.append(event_id)
                else:
                    self.LIST.addItem(
                        event_title + '| '+'[COLOR yellow]Starts : %s[/COLOR]' % start_time)
                    Item_Title.append(event_title+'|'+str(start_unix))
                    Item_Link.append(event_id)
            elif picked == 'other' and 'football' not in event.lower():
                info_string = info_string + \
                    ("[COLOR lime]%s[/COLOR] \nStarts: %s\nEnds: %s\n\n" %
                     (event_title, start_time, end_time))
                if live_now >= start_unix:
                    self.LIST.addItem(event_title + '| ' +
                                      '[COLOR lime]LIVE NOW[/COLOR]')
                    Item_Title.append(event_title+'|'+str(start_unix))
                    Item_Link.append(event_id)
                else:
                    self.LIST.addItem(
                        event_title + '| '+'[COLOR yellow]Starts : %s[/COLOR]' % start_time)
                    Item_Title.append(event_title+'|'+str(start_unix))
                    Item_Link.append(event_id)
            elif picked == 'Motorsports' and 'motorsports' in event.lower():
                info_string = info_string + \
                    ("[COLOR lime]%s[/COLOR] \nStarts: %s\nEnds: %s\n\n" %
                     (event_title, start_time, end_time))
                if live_now >= start_unix:
                    self.LIST.addItem(event_title + '| ' +
                                      '[COLOR lime]LIVE NOW[/COLOR]')
                    Item_Title.append(event_title+'|'+str(start_unix))
                    Item_Link.append(event_id)
                else:
                    self.LIST.addItem(
                        event_title + '| '+'[COLOR yellow]Starts : %s[/COLOR]' % start_time)
                    Item_Title.append(event_title+'|'+str(start_unix))
                    Item_Link.append(event_id)
    self.EventBox.setText(
        "[COLOR aqua]LIVE AND UPCOMING EVENTS[/COLOR]\n\n"+info_string)


def Go_Premium(self):
    dialog.ok(AddonTitle, "Premium Section Coming Soon")


def send_report(problem):
    streams = []
    for links in Item_Title:
        if not 'found by sportie' in links.lower():
            streams.append('[COLOR aqua]'+links+'[/COLOR]')
    if problem == 1:
        pass
    else:
        select = dialog.select(
            '[COLOR red]Please Select Link That Has An Issue[/COLOR]', streams)
        if select < 0:
            quit()
        if problem == 2:
            issue_to_report = 'Link not Working : %s'
        elif problem == 3:
            issue_to_report = 'Link buffering lots : %s'
        elif problem == 4:
            issue_to_report = 'Link showing wrong content : %s'
        live_now = int(time.time())
        test = streams[select].split('|')[1].replace('[/COLOR]', '')
        test = int(test)
        if live_now >= test:
            data = {'error': issue_to_report % streams[select].replace(
                '[COLOR aqua]', '').replace('[/COLOR]', '')}
            response = requests.post(error_api, data=data)
            dialog.ok(AddonTitle, "[COLOR red]%s[/COLOR]" % response.text)
        else:
            dialog.ok(
                AddonTitle, "This event hasn't started yet! You can only report once the event is live")


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
            self.LIST.addItem("Link Not Working - Event is now Live")
            issues.append(2)
            self.LIST.addItem("Link Buffering Lots")
            issues.append(3)
            self.LIST.addItem("Link showing wrong content")
            issues.append(4)
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


class Main(pyxbmct.AddonFullWindow):
    xbmc.executebuiltin("Dialog.Close(busydialog)")

    def __init__(self, title='sportie'):
        super(Main, self).__init__(title)
        self.setGeometry(1280, 720, 150, 50)
        self.main_bg_img = Background_Image
        self.main_bg = xbmcgui.ControlImage(0, 0, 1280, 720, self.main_bg_img)
        self.main_bg.setImage(Background_Image)
        self.addControl(self.main_bg)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, lambda: CloseWindow(self))
        self.connect(self.Error_button, lambda: Report_Issue())
        self.ChatBox = pyxbmct.TextBox()
        self.placeControl(self.ChatBox, 112, 18, 54, 32)
        self.ChatBox.autoScroll(2000, 800, 2000)

        self.EventBox = pyxbmct.TextBox()
        self.placeControl(self.EventBox, -6, 1, 170, 16)
        self.EventBox.autoScroll(1500, 800, 1)
        get_events(self)
        self.setFocus(self.LIST)
        self.connect(self.LIST, lambda: resolve_stream(
            Media_Title, Media_Link))

    def set_info_controls(self):
        # T L H W
        self.TIME = pyxbmct.Label('', textColor='0xFFFFFFFF', font='font16')
        self.placeControl(self.TIME, 10, 18, 10, 20)
        time2 = time.strftime("[COLOR yellow]%H:%M %p[/COLOR]")
        self.TIME.setLabel(str(time2))

    def Multi_Update(self):
        tick(self)
        self.list_update()
        Data.report_to_api()

    def set_active_controls(self):
        # T L H W

        self.Error_button = pyxbmct.Button(
            '',   focusTexture=errorS,   noFocusTexture=errorNS)
        self.placeControl(self.Error_button, 113, 22, 50, 10)

        self.Quit_button = pyxbmct.Button(
            '',   focusTexture=QuitS,   noFocusTexture=QuitNS)
        self.placeControl(self.Quit_button, 113, 36, 50, 10)

        # self.Premium_button = pyxbmct.Button('',   focusTexture=PremiumS,   noFocusTexture=PremiumNS)
        # self.placeControl(self.Premium_button, 113, 39, 50, 10)

        self.connect(self.Quit_button, lambda: CloseWindow(self))
        # self.connect(self.Premium_button, lambda:Go_Premium(self))
        self.LIST = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture=List_NFocused, _imageWidth=1,
                                 _imageHeight=2, _space=2, _itemHeight=50,  _itemTextXOffset=6, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
        self.placeControl(self.LIST, 19, 19, 90, 30)
        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.Multi_Update)

    def set_navigation(self):
        # DOWN
        self.LIST.controlDown(self.Error_button)
        # UP
        self.Error_button.controlUp(self.LIST)
        self.Quit_button.controlUp(self.LIST)
        # self.Premium_button.controlUp(self.LIST)
        # RIGHT
        self.LIST.controlRight(self.Error_button)
        # self.Quit_button.controlRight(self.Premium_button)
        self.Error_button.controlRight(self.Quit_button)
        # LEFT
        self.LIST.controlLeft(self.Error_button)
        # self.Premium_button.controlLeft(self.Quit_button)
        self.Quit_button.controlLeft(self.Error_button)

    def list_update(self):
        global Media_Title
        global Media_Link
        try:
            if self.getFocus() == self.LIST:
                position = self.LIST.getSelectedPosition()
                Media_Title = Item_Title[position]
                Media_Link = Item_Link[position]
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=slide  start=2000 end=0 time=1000',),
                               ('WindowClose', 'effect=rotatey  start=0 end=100 time=1000',)])


if __name__ == '__main__':
    MainWindow(user_choice)
