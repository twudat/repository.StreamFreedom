#############################################################
#################### START ADDON IMPORTS ####################
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2
import pyxbmct
import os
import re
import sys
import requests
import videos
from bs4 import BeautifulSoup
import updatecheck

translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
dialog = xbmcgui.Dialog()


#############################################################
#################### SET ADDON ID ###########################
_addon_id_ = 'plugin.video.fapzone'
AddonTitle = '[COLOR red]FapZone 18+ Only[/COLOR]'
_self_ = xbmcaddon.Addon(id=_addon_id_)
base_domain = 'https://eporner.com'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
headers = {'User-Agent': ua}
#############################################################
#################### SET ADDON THEME DIRECTORY ##############
_theme_ = _self_.getSetting('Theme')
_images_ = '/resources/' + _theme_

#############################################################
#################### SET ADDON THEME IMAGES #################
Background_Image = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'BG.jpg'))
# Background_Logo	= translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'model.gif'))
# Background_Logo1	= translatePath(os.path.join('special://home/addons/' + _addon_id_ + _images_, 'welcome.gif'))
Listbg = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'listbg.png'))
Addon_Image = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'model.gif'))
Addon_Icon = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'Addon_Icon.png'))
SearchF = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'searchs.png'))
SearchNF = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'searchns.png'))
List_Focused = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'ListBGS.png'))
List_NFocused = translatePath(os.path.join(
    'special://home/addons/' + _addon_id_ + _images_, 'ListBgNS.png'))


#############################################################
########## Function To Call That Starts The Window ##########
def MainWindow():
    global data
    global List
    window = Porn('fapzone')
    window.doModal()
    del window
    # xbmc.executebuiltin("Dialog.Close(busydialog)")


def passed(self, title):
    global CatUrls1
    global CatUrls2

    global iconUrls1
    global iconUrls2
    self.LIST1.reset()
    self.LIST1.setVisible(True)

    TotalCats = 0
    list1 = []
    list2 = []
    CatUrls1 = []
    CatUrls2 = []
    iconUrls1 = []
    iconUrls2 = []
    self.LIST1.addItem('[COLOR pink][B]FapZone[/B][/COLOR]')
    self.LIST2.addItem('[COLOR pink][B]FapZone[/B][/COLOR]')
    CatUrls1.append('')
    CatUrls2.append('')
    iconUrls1.append(Addon_Icon)
    iconUrls2.append(Addon_Icon)

    url = 'https://www.eporner.com/categories/'
    c = requests.get(url, headers=headers).text
    soup = BeautifulSoup(c, 'html5lib')
    content = soup.find_all('div', class_={'ctbinner'})
    for i in content:
        TotalCats += 1
        if (TotalCats % 2) == 0:
            list2.append(i)
        else:
            list1.append(i)
    for data in list1:
        try:
            name = data.a['title']
            url = data.a['href']
            icon = data.img['src']
            if not base_domain in url:
                url = base_domain+url
            CatUrls1.append(url)
            iconUrls1.append(icon)
            self.LIST1.addItem('[B]%s[/B]' % name)
        except:
            pass
    for data in list2:
        try:
            name = data.a['title']
            url = data.a['href']
            icon = data.img['src']
            if not base_domain in url:
                url = base_domain+url
            CatUrls2.append(url)
            iconUrls2.append(icon)
            self.LIST2.addItem('[B]%s[/B]' % name)
        except:
            pass


def Search(self):
    string = ''
    keyboard = xbmc.Keyboard(
        string, '[COLOR red]What Would You Like To Find?[/COLOR]')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        string = string.replace(' ', '-')
        if len(string) > 1:
            Media_Link = 'https://www.eporner.com/search/' + string
            videos.videowindow(Media_Link)
        else:
            quit()


def killaddon(self):

    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    self.close()
    self.close()


def List_Selected(self, OpenUrl):

    videos.videowindow(OpenUrl)

#############################################################
######### Class Containing the GUi Code / Controls ##########


class Porn(pyxbmct.AddonFullWindow):

    xbmc.executebuiltin("Dialog.Close(busydialog)")

    def __init__(self, title=''):
        super(Porn, self).__init__(title)

        self.setGeometry(1280, 720, 100, 50)

        Background = pyxbmct.Image(Background_Image)

        self.placeControl(Background, -10, -1, 123, 52)

        self.set_info_controls()

        self.set_active_controls()

        self.set_navigation()

        self.connect(pyxbmct.ACTION_NAV_BACK, lambda: killaddon(self))
        # self.connect(self.LIST1, lambda:List_Selected(self))
        self.connect(self.LIST1, lambda: List_Selected(self, OpenUrl))
        self.connect(self.LIST2, lambda: List_Selected(self, OpenUrl))
        self.connect(self.button1, lambda: Search(self))
        # self.setFocus(self.button1)

        passed(self, title)
        self.setFocus(self.LIST1)

    def set_info_controls(self):
        self.Hello = pyxbmct.Label(
            '', textColor='0xFFFFD700', font='font60', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self.Hello, -4, 1, 1, 50)

        # self.List =	pyxbmct.List(buttonFocusTexture=Listbg,_space=9,_itemTextYOffset=-7,textColor='0xFFFFD700')
        # self.placeControl(self.List, 0, 2, 115, 10)
        self.LIST1 = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture=List_NFocused, _imageWidth=1,
                                  _imageHeight=2, _space=2, _itemHeight=50,  _itemTextXOffset=30, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
        self.placeControl(self.LIST1, 13, 15, 104, 10)
        self.LIST2 = pyxbmct.List(buttonFocusTexture=List_Focused, buttonTexture=List_NFocused, _imageWidth=1,
                                  _imageHeight=2, _space=2, _itemHeight=50,  _itemTextXOffset=30, _itemTextYOffset=-2, textColor='0xFFFFFFFF')
        self.placeControl(self.LIST2, 13, 25, 104, 10)

        # self.textbox = pyxbmct.TextBox(textColor='0xFFFFD700')
        # self.placeControl(self.textbox, 95, 18, 30, 30)

        self.Show_Logo = pyxbmct.Image('')
        self.placeControl(self.Show_Logo, -6, 41, 37, 8)

        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.List_update)

    def set_active_controls(self):

        self.button1 = pyxbmct.Button(
            '',   noFocusTexture=SearchNF, focusTexture=SearchF)
        self.placeControl(self.button1, 90, 36,  18, 4)

        # self.button11 = pyxbmct.Button('',   noFocusTexture=Addon_Icon, focusTexture=Addon_Icon)
        # self.placeControl(self.button11, -4, 42,  20, 8)
        # self.button12 = pyxbmct.Button('',   noFocusTexture=Background_Logo1, focusTexture=Background_Logo1)
        # self.placeControl(self.button12, -4, 16,  25, 26)

    def set_navigation(self):
        self.LIST1.controlRight(self.LIST2)
        self.LIST2.controlLeft(self.LIST1)
        self.LIST2.controlRight(self.button1)
        self.button1.controlLeft(self.LIST2)

    def List_update(self):
        global OpenUrl

        try:
            if self.getFocus() == self.LIST1:
                Focus = self.LIST1.getSelectedPosition()
                self.LIST2.selectItem(Focus)
                # Media_Title = Item_Title[Focus]
                # Media_Link  = CatUrls1[Focus]
                Media_Icon = iconUrls1[Focus]
                OpenUrl = CatUrls1[Focus]
            elif self.getFocus() == self.LIST2:
                Focus = self.LIST2.getSelectedPosition()
                self.LIST1.selectItem(Focus)
                # Media_Title = Item_Title[Focus]
                Media_Link = CatUrls2[Focus]
                Media_Icon = iconUrls2[Focus]
                OpenUrl = CatUrls2[Focus]
            self.Show_Logo.setImage(Media_Icon)
        except (RuntimeError, SystemError):
            pass


updatecheck.checkupdates()
if __name__ == '__main__':
    MainWindow()
