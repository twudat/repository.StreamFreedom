# Deobfuscated by StreamFreedom from XXX-O-DUS version="5.00.023"
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
import Cats
from datetime import datetime
import random
import string
import re
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
AppIcon = xbmcvfs.translatePath(os.path.join(Skin_Path, 'AppIcon.png'))
AppTitle = xbmcvfs.translatePath(os.path.join(Skin_Path, 'AppTitle3.gif'))
LiveF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'LiveF1.png'))
LiveNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'LiveNF.png'))
CamF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'CamF1.png'))
CamNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'CamNF.png'))
MoviesF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'MoviesF1.png'))
MoviesNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'MoviesNF.png'))
SitesF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'SitesF1.png'))
SitesNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'SitesNF.png'))
ExitF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'ExitF1.png'))
ExitNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'ExitNF.png'))
SendF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'MessageF1.png'))
SendNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'MessageNF.png'))
RefreshF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'RefreshF1.png'))
RefreshNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'RefreshNF.png'))
UserF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'UserchangeF2.png'))
UserNF = xbmcvfs.translatePath(os.path.join(Skin_Path, 'UserchangeNF1.png'))
BackgroundBox = xbmcvfs.translatePath(os.path.join(Skin_Path, 'BackBox.png'))
AddonInfoUrl = 'https://pinsystem.co.uk/CumWithMe/CumWithMeNotice.txt'
ChatMsgsUrl = 'https://pinsystem.co.uk/CumWithMe/Chat/getmsg.php'
ChatMsgSendurl = 'https://pinsystem.co.uk/CumWithMe/Chat/addmsg.php?user=%s&msg=%s'
ApiUrl = 'https://pinsystem.co.uk/CumWithMe/api.php'
CheckMonitor = get_setting('Monitor')
if CheckMonitor == 'false':
    CheckMon = '[COLOR red]OFF[/COLOR]'
if CheckMonitor == 'true':
    CheckMon = '[COLOR lime]ON[/COLOR]'


def CheckPin():
    return # StreamFreedom patch
    pin = get_setting('PinCode')
    if pin == '':
        pin = 'EXPIRED'
    if pin == 'EXPIRED':
        set_setting('pinused', 'False')
        dialog.ok(AddonTitle, "[COLOR yellow]Please visit [COLOR magenta]https://pinsystem.co.uk[COLOR yellow] to generate an Access Token For [COLOR magenta]CumWithMe[COLOR yellow] then enter it after clicking ok[/COLOR]")
        string = ''
        keyboard = xbmc.Keyboard(
            string, '[COLOR red]Please Enter Pin Generated From Website[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            string = keyboard.getText()
            if len(string) > 1:
                term = string.title()
                set_setting('PinCode', term)
                CheckPin()
            else:
                quit()
        else:
            quit()
    if not 'EXPIRED' in pin:
        pinurlcheck = (
            'https://pinsystem.co.uk/service.php?code=%s&plugin=RnVja1lvdSE' % pin)
        link = requests.get(pinurlcheck).text
        if len(link) <= 2 or 'Pin Expired' in link:
            set_setting('PinCode', 'EXPIRED')
            CheckPin()
        else:
            registerpin = get_setting('pinused')
            if registerpin == 'False':
                try:
                    requests.get(
                        'https://pinsystem.co.uk/checker.php?code=99999&plugin=CumWithMe').text
                    set_setting('pinused', 'True')
                except:
                    pass
            else:
                pass


def MainWindow():
    window = Main('cwm')
    window.doModal()
    del window


def MoveToCat(self, option):
    ApiInfo(self)
    Cats.MainWindow(option)


def tick(self):
    time2 = time.strftime("%I:%M %p")
    self.TIME.setLabel(str(time2))


def QuitAddon(self):
    try:
        CheckUserID = get_setting('userid')
        removeuser = requests.get(
            'https://pinsystem.co.uk/CumWithMe/removeuser.php?user=%s' % CheckUserID)
        set_setting('userid', '')
    except:
        pass
    xbmc.executebuiltin("Container.Update(path,replace)")
    xbmc.executebuiltin("ActivateWindow(Home)")
    self.close()


def GetAddonInfo(self):
    link = requests.get(AddonInfoUrl).text
    self.AddonTextInfo.setText(link)


def GetChatMsgs(self):
    ApiInfo(self)
    chatboxshow = get_setting('ShowChat')
    if chatboxshow == 'true':
        try:
            link = requests.get(ChatMsgsUrl).json()
            messages = []
            reservednames = ["nemzzy", "nemzzzy", "nemzzyy", "nemesis",
                             "nemzzy668", "manc", "_manc", "_manc_", "lordjd", "jdlord"]
            for i in link:
                Name = i['items']['Name']
                Message = i['items']['Message']
                Time = i['items']['Time']
                if any(x in Name.lower() for x in reservednames):
                    Msg = (
                        '[COLOR magenta]%s : [COLOR purple]%s -  [COLOR white]%s[/COLOR]\n' % (Time, Name, Message))
                else:
                    Msg = (
                        '[COLOR magenta]%s : [COLOR green]%s -  [COLOR white]%s[/COLOR]\n' % (Time, Name, Message))
                messages.append(Msg)
            chatstring = ''
            for message in messages:
                chatstring = chatstring+message
            self.ChatBox.setText(chatstring)
            dialog.notification(
                AddonTitle, '[COLOR pink]Chat Window Refreshed[/COLOR]', AddonIcon, 2500)
            GetAddonInfo(self)
        except:
            self.ChatBox.setText(
                '[COLOR magenta]Admin Message : [COLOR purple]Nemzzy -  [COLOR white]Welcome to CumWithMe, Enjoy the chat room, don\'t be a keyboard warrior! Your not hard, not yet anyway! Enjoy the porn[/COLOR]\n')
    else:
        self.ChatBox.setText(
            '[COLOR magenta]Admin Message : [COLOR purple]Nemzzy -  [COLOR white]You\'ve turned chat off in settings, turn on again to show messages[/COLOR]\n')


def SendChatMsg(self):
    checkusername = get_setting('Username')
    reservednames = ["nemzzy", "nemzzzy", "nemzzyy", "nemesis", "nemzzy668", "manc", "_manc", "_manc_", "lordjd",
                     "jdlord", "admin", "nemz", "jd", "nemz", "streamarmy", "streamarmyteam", "streamarmyadmin", "adminstreamarmy"]
    if any(x in checkusername.lower() for x in reservednames):
        checkadmin = get_setting('adminchatpass')
        if checkadmin.lower() == 'manclovescock':
            pass
        else:
            dialog.ok(
                AddonTitle, "You have tried to use a name reserved for Stream Army Team Members, Please enter the password to continue")
            string = ''
            keyboard = xbmc.Keyboard(
                string, '[COLOR white][B]Enter Password[/B][/COLOR]')
            keyboard.doModal()
            if keyboard.isConfirmed():
                string = keyboard.getText()
                if string.lower() == 'manclovescock':
                    set_setting(id='adminchatpass', value=string.lower())
                    SendChatMsg(self)
                else:
                    dialog.ok(
                        AddonTitle, "Wrong Password, Please Choose A Different Chat Name")
                    set_setting(id='Username', value='')
                    SendChatMsg(self)
            else:
                quit()
    if checkusername == '':
        string = ''
        keyboard = xbmc.Keyboard(
            string, '[COLOR magenta][B]You need to set a chat username first ( Some Admin Names reserved! )[/B][/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            string = keyboard.getText()
            if len(string) > 1:
                term = string.lower()
                if not any(x in term.lower() for x in reservednames):
                    if len(string) > 1:
                        set_setting(id='Username', value=string.title())
                        SendChatMsg(self)
                else:
                    dialog.ok(
                        AddonTitle, "You have tried to use a name reserved for Stream Army Team Members, Please enter the password to continue")
                    stringpass = ''
                    keyboard = xbmc.Keyboard(
                        stringpass, '[COLOR white][B]Enter Password[/B][/COLOR]')
                    keyboard.doModal()
                    if keyboard.isConfirmed():
                        stringpass = keyboard.getText()
                        if stringpass.lower() == 'manclovescock':
                            set_setting(id='adminchatpass',
                                        value=stringpass.lower())
                            set_setting(id='Username', value=string.title())
                            SendChatMsg(self)
                        else:
                            dialog.ok(
                                AddonTitle, "Wrong Password, Please Choose A Different Chat Name")
                            SendChatMsg(self)
        else:
            quit()
    else:
        string = ''
        keyboard = xbmc.Keyboard(
            string, '[COLOR magenta][B]Type Chat Message ( Don\'t be offensive )[/B][/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            string = keyboard.getText()
            if len(string) > 1:
                term = string.lower()
                term = term.replace(' ', '%20')
                sendmessage = requests.get(
                    ChatMsgSendurl % (checkusername, term))
                dialog.notification(
                    AddonTitle, '[COLOR pink]Message Sent[/COLOR]', AddonIcon, 2500)
                GetChatMsgs(self)
            else:
                dialog.notification(
                    AddonTitle, '[COLOR pink]Message needs to be longer[/COLOR]', AddonIcon, 2500)


def RandomUserID(self):
    CheckClean = get_setting('userid')
    if CheckClean == '':
        UserID = (''.join(random.choices(string.ascii_uppercase, k=5)))
        set_setting('userid', UserID)
        adduser = requests.get(
            'https://pinsystem.co.uk/CumWithMe/adduser.php?user=%s' % UserID)
    else:
        removeuser = requests.get(
            'https://pinsystem.co.uk/CumWithMe/removeuser.php?user=%s' % CheckClean)
        set_setting('userid', '')
        RandomUserID(self)


def ApiInfo(self):
    try:
        link = requests.get(ApiUrl).json()
        for data in link:
            usersonline = data['usercount']['Users']
            camsonline = data['usercount']['CamsOnline']
            videos = data['usercount']['Videos']
            self.USERS.setLabel('Current Cummers Online : %s' % usersonline)
            self.CHANNELS.setLabel('Live Cams Online : %s' % camsonline)
            self.MOVIES.setLabel('Movies Available : %s' % videos)
    except:
        pass


def ChangeUserName(self):
    reservednames = ["nemzzy", "nemzzzy", "nemzzyy", "nemesis", "nemzzy668", "manc", "_manc", "_manc_", "lordjd",
                     "jdlord", "admin", "nemz", "jd", "nemz", "streamarmy", "streamarmyteam", "streamarmyadmin", "adminstreamarmy"]
    string = ''
    keyboard = xbmc.Keyboard(
        string, '[COLOR magenta][B]Change User Name[/B][/COLOR]')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string) > 3:
            term = string.title()
            if any(x in term.lower() for x in reservednames):
                checkadmin = get_setting('adminchatpass')
                if checkadmin.lower() == 'manclovescock':
                    set_setting('Username', term)
                    dialog.notification(
                        AddonTitle, '[COLOR pink]Username Set[/COLOR]', AddonIcon, 2500)
                else:
                    dialog.ok(
                        AddonTitle, "You have tried to use a name reserved for Stream Army Team Members, Please enter the password to continue")
                    string = ''
                    keyboard = xbmc.Keyboard(
                        string, '[COLOR white][B]Enter Password[/B][/COLOR]')
                    keyboard.doModal()
                    if keyboard.isConfirmed():
                        string = keyboard.getText()
                        if string.lower() == 'manclovescock':
                            set_setting(id='adminchatpass',
                                        value=string.lower())
                            set_setting('Username', term)
                            dialog.notification(
                                AddonTitle, '[COLOR pink]Username Set[/COLOR]', AddonIcon, 2500)
                        else:
                            dialog.ok(
                                AddonTitle, "Wrong Password, Please Choose A Different Chat Name")
                            set_setting(id='Username', value='')
                            ChangeUserName(self)
                    else:
                        quit()
            else:
                set_setting('Username', term)
                dialog.notification(
                    AddonTitle, '[COLOR pink]Username Set[/COLOR]', AddonIcon, 2500)
        else:
            dialog.notification(
                AddonTitle, '[COLOR pink]Username needs to be longer[/COLOR]', AddonIcon, 2500)


def ScraperCheck(self):
    try:
        scrappercurrent = requests.get(
            'https://raw.githubusercontent.com/nemesis668/repository.streamarmy18-19/main/script.cwm.scrapers/addon.xml').text
        currentversion = re.findall(
            '<addon id="script.cwm.scrapers".*?version="(.*?)"', scrappercurrent, flags=re.DOTALL)[0]
        scrapertheirs = xbmcvfs.translatePath(os.path.join(
            'special://home/addons/' + 'script.cwm.scrapers', 'addon.xml'))
        with open(scrapertheirs) as f:
            yourversion = re.findall(
                '<addon id="script.cwm.scrapers".*?version="(.*?)"', f.read(), flags=re.DOTALL)[0]
        if currentversion > yourversion:
            ColorCode = 'red'
        else:
            ColorCode = 'lime'
        self.ScraperInfo = pyxbmct.Label('[B]Scraper Info : Your Scrapers : [COLOR %s]%s[/COLOR] - Most Current Scrapers : %s[/B]' % (
            ColorCode, yourversion, currentversion), textColor='0xFFFFFFFF', font='font12', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self.ScraperInfo,  12, 10, 12, 40)
    except:
        self.ScraperInfo = pyxbmct.Label(
            '[B]Scraper Info : Can\'t get current scraper information[/B]', textColor='0xFFFFFFFF', font='font12')
        self.placeControl(self.ScraperInfo,  12, 10, 12, 40)


class Main(pyxbmct.AddonFullWindow):
    xbmc.executebuiltin("Dialog.Close(busydialog)")

    def __init__(self, title='cwm'):
        super(Main, self).__init__(title)
        self.setGeometry(1280, 720, 150, 50)
        self.main_bg_img = Background_Image
        self.main_bg = xbmcgui.ControlImage(0, 0, 1280, 720, self.main_bg_img)
        self.main_bg.setImage(Background_Image)
        self.addControl(self.main_bg)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, lambda: QuitAddon(self))
        AppLogo = pyxbmct.Image(AppIcon)
        self.placeControl(AppLogo, -10, 45, 30, 6)
        AppHeader = pyxbmct.Image(AppTitle)
        self.placeControl(AppHeader, -47, -4, 90, 27)
        BackBox = pyxbmct.Image(BackgroundBox)
        self.placeControl(BackBox, 14, 9, 136, 44)
        self.AddonInfo = pyxbmct.Label(
            '[B]ADDON INFORMATION[/B]', textColor='0xFFFFFFFF', font='font14')
        self.placeControl(self.AddonInfo,  20, 26, 12, 15)
        self.ChatInfo = pyxbmct.Label(
            '[B]CHAT ROOM[/B]', textColor='0xFFFFFFFF', font='font14')
        self.placeControl(self.ChatInfo,  84, 26, 12, 15)
        self.AddonTextInfo = pyxbmct.TextBox()
        self.placeControl(self.AddonTextInfo, 26, 14, 60, 34)
        self.AddonTextInfo.autoScroll(1000, 1500, 2000)
        GetAddonInfo(self)
        self.setFocus(self.LiveChanBut)
        RandomUserID(self)
        self.ChatBox = pyxbmct.TextBox()
        self.placeControl(self.ChatBox, 90, 14, 54, 34)
        self.ChatBox.autoScroll(2000, 800, 2000)
        GetChatMsgs(self)
        ScraperCheck(self)

    def set_info_controls(self):
        self.TIME = pyxbmct.Label('', textColor='0xFFFFFFFF', font='font14')
        self.USERS = pyxbmct.Label('', textColor='0xFFFFFFFF', font='font14')
        self.CHANNELS = pyxbmct.Label(
            '', textColor='0xFFFFFFFF', font='font14')
        self.MonitorStatus = pyxbmct.Label(
            '', textColor='0xFFFFFFFF', font='font14')
        self.MOVIES = pyxbmct.Label('', textColor='0xFFFFFFFF', font='font14')
        self.placeControl(self.TIME, 158, 47, 12, 10)
        self.placeControl(self.USERS, 158, 0, 12, 20)
        self.placeControl(self.CHANNELS, 150, 0, 12, 20)
        self.placeControl(self.MonitorStatus, 150, 10, 12, 20)
        self.placeControl(self.MOVIES, 142, 0, 12, 20)
        time2 = time.strftime("%I:%M %p")
        self.TIME.setLabel(str(time2))
        self.USERS.setLabel('Current Cummers Online : ')
        self.CHANNELS.setLabel('Live Cams Available : ')
        self.MonitorStatus.setLabel(' | Monitor Status : %s' % CheckMon)
        self.MOVIES.setLabel('Movies Available : ')

    def Multi_Update(self):
        tick(self)

    def set_active_controls(self):
        # T L W H
        self.LiveChanBut = pyxbmct.Button(
            '',   focusTexture=LiveF,   noFocusTexture=LiveNF)
        self.placeControl(self.LiveChanBut, 10, 0, 30, 12)
        self.LiveCamBut = pyxbmct.Button(
            '',   focusTexture=CamF,   noFocusTexture=CamNF)
        self.placeControl(self.LiveCamBut, 40, 0, 30, 12)
        self.LiveMovieBut = pyxbmct.Button(
            '',   focusTexture=MoviesF,   noFocusTexture=MoviesNF)
        self.placeControl(self.LiveMovieBut, 70, 0, 30, 12)
        self.LiveSiteBut = pyxbmct.Button(
            '',   focusTexture=SitesF,   noFocusTexture=SitesNF)
        self.placeControl(self.LiveSiteBut, 100, 0, 30, 12)
        self.ExitSiteBut = pyxbmct.Button(
            '',   focusTexture=ExitF,   noFocusTexture=ExitNF)
        self.placeControl(self.ExitSiteBut, 130, 0, 15, 10)
        self.SendMsgBut = pyxbmct.Button(
            '',   focusTexture=SendF,   noFocusTexture=SendNF)
        self.placeControl(self.SendMsgBut, 143, 34, 20, 7)
        self.RefMsgBut = pyxbmct.Button(
            '',   focusTexture=RefreshF,   noFocusTexture=RefreshNF)
        self.placeControl(self.RefMsgBut, 143, 19, 20, 7)
        self.ChangeUserBut = pyxbmct.Button(
            '',   focusTexture=UserF,   noFocusTexture=UserNF)
        self.placeControl(self.ChangeUserBut, 143, 26, 20, 8)
        self.connect(self.ExitSiteBut, lambda: QuitAddon(self))
        self.connect(self.LiveChanBut, lambda: MoveToCat(self, 'Live'))
        self.connect(self.LiveCamBut, lambda: MoveToCat(self, 'Cam'))
        self.connect(self.LiveMovieBut, lambda: MoveToCat(self, 'Movie'))
        self.connect(self.LiveSiteBut, lambda: MoveToCat(self, 'Sites'))
        self.connect(self.RefMsgBut, lambda: GetChatMsgs(self))
        self.connect(self.SendMsgBut, lambda: SendChatMsg(self))
        self.connect(self.ChangeUserBut, lambda: ChangeUserName(self))
        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.Multi_Update)

    def set_navigation(self):
        # DOWN
        self.LiveChanBut.controlDown(self.LiveCamBut)
        self.LiveCamBut.controlDown(self.LiveMovieBut)
        self.LiveMovieBut.controlDown(self.LiveSiteBut)
        self.LiveSiteBut.controlDown(self.ExitSiteBut)
        # UP
        self.ExitSiteBut.controlUp(self.LiveSiteBut)
        self.LiveSiteBut.controlUp(self.LiveMovieBut)
        self.LiveMovieBut.controlUp(self.LiveCamBut)
        self.LiveCamBut.controlUp(self.LiveChanBut)
        # RIGHT
        self.LiveChanBut.controlRight(self.RefMsgBut)
        self.LiveCamBut.controlRight(self.RefMsgBut)
        self.LiveMovieBut.controlRight(self.RefMsgBut)
        self.LiveSiteBut.controlRight(self.RefMsgBut)
        self.ExitSiteBut.controlRight(self.RefMsgBut)
        self.RefMsgBut.controlRight(self.ChangeUserBut)
        self.ChangeUserBut.controlRight(self.SendMsgBut)
        # LEFT
        self.SendMsgBut.controlLeft(self.ChangeUserBut)
        self.RefMsgBut.controlLeft(self.LiveChanBut)
        self.ChangeUserBut.controlLeft(self.RefMsgBut)

    def list_update(self):
        pass


CheckPin()
if __name__ == '__main__':
    MainWindow()
