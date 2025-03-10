import sys, shutil, os
from urllib.parse import urlencode
from urllib.parse import parse_qsl

#from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import pyxbmct
import xml.etree.ElementTree as ET
# Get a pointer to the translatePath function
translatePath = xbmcvfs.translatePath

xxxodus_version="5.00.023"
# create a class for your addon, we need this to get info about your addon
TRGTADDON = xbmcaddon.Addon('plugin.video.xxx-o-dus')
TRGTNAME  = TRGTADDON.getAddonInfo('name')
TRGTVER   = TRGTADDON.getAddonInfo('version')



NEMZADDON = xbmcaddon.Addon('script.module.nemzzy')
THISADDON = xbmcaddon.Addon()
THISVERSN = THISADDON.getAddonInfo('version')
THISNAME  = THISADDON.getAddonInfo('name')
tgt_v     = int(TRGTVER.replace('.',''))
ths_v     = int(THISVERSN.replace('.',''))
req_v     = int(xxxodus_version.replace('.',''))
VERSAME   = (tgt_v == req_v)
AGETXT    = 'Newer'
older     = (tgt_v < req_v)
if older: AGETXT    = 'Older'


# get the full path to your addon, decode it to unicode to handle special (non-ascii) characters in the path
SRCDIR = THISADDON.getAddonInfo('path') #.decode('utf-8') <--- decode fails with:  AttributeError: 'str' object has no attribute 'decode'
TGTDIR = TRGTADDON.getAddonInfo('path') #.decode('utf-8') <--- decode fails with:  AttributeError: 'str' object has no attribute 'decode'
NEMZDIR = NEMZADDON.getAddonInfo('path') #.decode('utf-8') <--- decode fails with:  AttributeError: 'str' object has no attribute 'decode'


OURNAME  = THISADDON.getAddonInfo('name')
TRGTNAME = TRGTADDON.getAddonInfo('name')
NEMZNAME = NEMZADDON.getAddonInfo('name')

dialog = xbmcgui.Dialog()

REPLACES = {'/resources/lib/modules/': '/resources/patchfiles/lib/replace',
           '/'                      : '/resources/patchfiles/'}

ADDITIONS = {'/resources/lib/modules/': '/resources/patchfiles/lib/add'}

NEMZPATCH = { '/'                   : '/resources/patchfiles/nemmzy/'}

class TextBox(pyxbmct.AddonDialogWindow):
    def __init__(self, title='Info',Message=None,autoscroll=True):
        super(TextBox, self).__init__(title)
        self.setGeometry(950, 600, 10, 30, 0, 5, 5)
        self.set_info_controls(Message,autoscroll)
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self,msg,autoscroll):
        Background   = pyxbmct.Image(translatePath(os.path.join('special://home/addons/script.freexxxodus.artwork', 'resources/art/dialog/bg.jpg')))
        self.placeControl(Background, 0, 0, 10, 30)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 0, 1, 9, 28)
        self.textbox.setText(msg)
        Scroll=autoscroll
        if Scroll:
            self.textbox.autoScroll(1000, 2000, 1000)

        # self.autoscroll=autoscroll
class TextBox(pyxbmct.AddonDialogWindow):
    def __init__(self, title='Info',Message=None,autoscroll=True):
        super(TextBox, self).__init__(title)
        self.setGeometry(950, 600, 10, 30, 0, 5, 5)
        self.set_info_controls(Message,autoscroll)
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self,msg,autoscroll):
        Background   = pyxbmct.Image(translatePath(os.path.join('special://home/addons/script.freexxxodus.artwork', 'resources/art/dialog/bg.jpg')))
        self.placeControl(Background, 0, 0, 10, 30)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 0, 1, 9, 28)
        self.textbox.setText(msg)
        Scroll=autoscroll
        if Scroll:
            self.textbox.autoScroll(1000, 2000, 1000)

        # self.autoscroll=autoscroll

    def set_active_controls(self):
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 9,26,1,4)
        self.connect(self.button, self.close)

    def set_navigation(self):
        self.button.controlUp(self.button)
        self.button.controlDown(self.button)
        self.button.controlRight(self.button)
        self.button.controlLeft(self.button)
        self.setFocus(self.button)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])

    def set_active_controls(self):
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 9,26,1,4)
        self.connect(self.button, self.close)

    def set_navigation(self):
        self.button.controlUp(self.button)
        self.button.controlDown(self.button)
        self.button.controlRight(self.button)
        self.button.controlLeft(self.button)
        self.setFocus(self.button)

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=200',), ('WindowClose', 'effect=fade start=100 end=0 time=300',)])




# defaultbutton options
# xbmcgui.DLG_YESNO_NO_BTN     :Set the “No” button as default.
# xbmcgui.DLG_YESNO_YES_BTN    :Set the “Yes” button as default.
# xbmcgui.DLG_YESNO_CUSTOM_BTN :Set the “Custom” button as default.
# autoclose – [opt] integer - milliseconds to autoclose dialog. (default=do not autoclose)

if VERSAME:
    msg = "%s \n\nShall We Patch %s?\n(Will assume you're too chicken in 30 secs)" % ( OURNAME, TRGTNAME )

    ret = dialog.yesno(heading=OURNAME,message=msg,
                           nolabel="Nah, I'm too chicken",
                           yeslabel="Do it!",
                           autoclose=30000,
                           defaultbutton=xbmcgui.DLG_YESNO_NO_BTN)
    if ret == 1:
        msg=''
        # remove the dependancy on script.module.nemzzy from config.xml
        # this script is a service that does a lot of stuff nemzzy doesnt
        # want you to know about
        xmlfile = os.path.join(TGTDIR, 'addon.xml')
        if ( os.path.exists(xmlfile)):
            file = ET.parse(xmlfile)
            root = file.getroot()
            for elem in root.findall('.//requires'):
                nemzzy = elem.find('./import[@addon="script.module.nemzzy"]')
                if nemzzy is not None:
                    elem.remove(nemzzy)
                    os.rename(xmlfile,xmlfile+'.bak')
                    file.write(xmlfile)
                    msg+='Removed :\tnemzzy dependancy from %s \n' % xmlfile.split(".kodi/")[1]



        for tgt in REPLACES:
            src = REPLACES[tgt]
            srcdir =  os.path.join(SRCDIR, src[1:])
            tgtdir =  os.path.join(TGTDIR, tgt[1:])

            filelist = [os.path.join(srcdir, f) for f in os.listdir(srcdir) if os.path.isfile(os.path.join(srcdir, f))]
            # print(onlyfiles)
            for srcfile in filelist:
                shutil.copy(srcfile,tgtdir)
                msg+='Replaced :\t%s%s\n' % (tgtdir.split(".kodi/")[1],os.path.basename(srcfile))

        for tgt in ADDITIONS:
            src = ADDITIONS[tgt]
            srcdir =  os.path.join(SRCDIR, src[1:])
            tgtdir =  os.path.join(TGTDIR, tgt[1:])

            filelist = [os.path.join(srcdir, f) for f in os.listdir(srcdir) if os.path.isfile(os.path.join(srcdir, f))]
            # print(onlyfiles)
            for srcfile in filelist:
                shutil.copy(srcfile,tgtdir)
                msg+='Added :\t%s%s\n' % (tgtdir.split(".kodi/")[1],os.path.basename(srcfile))

        msgprmpt = "%s \n\nShall We Kill the Nemzzy Service too?%s?\n(Will assume you're too chicken in 30 secs)" % ( OURNAME, TRGTNAME )

        ret = dialog.yesno(heading=OURNAME,message=msgprmpt,
                               nolabel="Nah, I'm too chicken",
                               yeslabel="Do it!",
                               autoclose=30000,
                               defaultbutton=xbmcgui.DLG_YESNO_NO_BTN)
        if ret == 1:
            # msg+='Nemzzy dir = %s\n' % NEMZDIR
            for tgt in NEMZPATCH:
                src = NEMZPATCH[tgt]
                srcdir =  os.path.join(SRCDIR, src[1:])
                tgtdir =  os.path.join(NEMZDIR, tgt[1:])
                filelist = [os.path.join(srcdir, f) for f in os.listdir(srcdir) if os.path.isfile(os.path.join(srcdir, f))]
                # print(onlyfiles)
                for srcfile in filelist:
                    shutil.copy(srcfile,tgtdir)
                    msg+='Patched :\t%s%s\n' % (tgtdir.split(".kodi/")[1],os.path.basename(srcfile))


        window = TextBox(Message=msg)
        window.doModal()
        del window
else:
    msg ="%s version %s was written for %s version %s\n" % (THISNAME,THISVERSN, TRGTNAME, xxxodus_version )

    msg+="You have %s version %s which is %s\n" % (TRGTNAME, TRGTVER, AGETXT)
    if older :
        msg+="You could try updating %s %s\n"  % (TRGTNAME, TRGTVER )
    else:
        msg+="You could try updating %s\n"  % THISNAME
    msg+="If that doesnt work try making contact on GitHub\n"


    window = TextBox(Message=msg)
    window.doModal()
    del window
