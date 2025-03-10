import sys, shutil, os ,re
from urllib.parse import urlencode
from urllib.parse import parse_qsl
import requests
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

# xxxodus_version="5.00.023"
# import web_pdb; web_pdb.set_trace()

# NEMZADDON = xbmcaddon.Addon('script.module.nemzzy')
THISADDON = xbmcaddon.Addon()
THISVERSN = THISADDON.getAddonInfo('version')
THISNAME  = THISADDON.getAddonInfo('name')
THISID    = THISADDON.getAddonInfo('id')
# tgt_v     = int(TRGTVER.replace('.',''))
# ths_v     = int(THISVERSN.replace('.',''))
# req_v     = int(xxxodus_version.replace('.',''))
# VERSAME   = (tgt_v == req_v)
# AGETXT    = 'Newer'
# older     = (tgt_v < req_v)
# if older: AGETXT    = 'Older'


# get the full path to your addon, decode it to unicode to handle special (non-ascii) characters in the path
SRCDIR = os.path.join(THISADDON.getAddonInfo('path'),"resources/patchfiles/") #.decode('utf-8') <--- decode fails with:  AttributeError: 'str' object has no attribute 'decode'



dialog = xbmcgui.Dialog()

streamarmyxml = 'https://raw.githubusercontent.com/nemesis668/repository.streamarmy18-19/main/addons.xml'
streamarmy_pattern = r'''<addon\sid=['"](plugin.*?)['"]'''
releasedaddons = []

DEBUG=False

def DLog(message="" ):
    if DEBUG and message!="":
        msg="StreamFreedom >> %s" % message
        xbmc.log( msg=msg, level=xbmc.LOGINFO)
        dialog.ok('Debug',message)



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

def list_files(filepath):
    paths = []
    for path, dirs, files in os.walk(filepath):
        for file in files:
            fp=os.path.join(path, file)
            if os.path.isfile(fp):
                paths.append(fp)
    return(paths)


msg=""
err=""
def runpatch(addon):
    # if DEBUG and (addon != 'plugin.video.xxx-o-dus'): return
    global msg , err
    DLog("Runpatch : %s" % addon)
    # create a class for your addon, we need this to get info about your addon
    # xbmcvfs.translatePath()
    addonxml = xbmcvfs.translatePath(os.path.join(
        'special://home/addons/%s' % addon, 'addon.xml'))
    if os.path.exists(addonxml):
        try:
            TRGTADDON = xbmcaddon.Addon(addon)
            TRGTNAME  = TRGTADDON.getAddonInfo('name')
            TRGTVER   = TRGTADDON.getAddonInfo('version')
            TGTDIR    = TRGTADDON.getAddonInfo('path') #.decode('utf-8') <--- decode fails with:  AttributeError: 'str' object has no attribute 'decode'
        except:
            msg += '%s\t seems to be installed but no xml file was found!\n' % addon
            return
    else:
        msg += '%s\t does not seem to be installed!\n' % addon
        return

    srcdir =  os.path.join(SRCDIR, addon)
    if os.path.isdir(srcdir):
        dlgmsg = "Shall We Patch %s?\n\n\n(Will assume you're too chicken in 30 secs)" % TRGTNAME

        ret = dialog.yesno(heading="Patch %s" % TRGTNAME, message=dlgmsg,
                           nolabel="Nah, I'm too chicken",
                           yeslabel="Do it!",
                           autoclose=30000,
                           defaultbutton=xbmcgui.DLG_YESNO_NO_BTN)
        kw = "Did not patch"
        if ret == 1:
            # msg = ''
            filelist = list_files(srcdir)#[os.path.join(srcdir, f) for f in os.listdir(srcdir) if os.path.isfile(os.path.join(srcdir, f))]
            for srcfile in filelist:
                kw="Added"
                trgtfile=srcfile.split("/plugin.video.StreamFreedom/resources/patchfiles/")[1]
                trgtfile=xbmcvfs.translatePath(os.path.join('special://home/addons/%s' % trgtfile))

                DLog("Copy %s to\n%s" % ( srcfile , trgtfile))
                if os.path.isfile(trgtfile):
                    kw="Replace"
                if not DEBUG:
                    shutil.copy(srcfile,os.path.dirname(trgtfile))
                else:
                    kw="Simulated %s" % kw
                # msg+='%s :\t%s%s\n' % (kw, TGTDIR.split(".kodi/")[1],os.path.basename(srcfile))
                msg+='\n%s  :\n%s\nto\n%s\n' % (kw, srcfile.split(".kodi/")[1],trgtfile.split(".kodi/")[1])
        else:
            msg += '%s\t was not patched by your request\n' % addon
    # else:
    #     err="%s\n%s\n%s\n\n" % (err,SRCDIR, addon)
        # dialog.ok("Not Found",addon)


    # remove the dependancy on script.module.nemzzy from config.xml
    # this script is a service that does a lot of stuff nemzzy doesnt
    # want you to know about

    file = ET.parse(addonxml)
    root = file.getroot()
    for elem in root.findall('.//requires'):
        nemzzy = elem.find('./import[@addon="script.module.nemzzy"]')
        if nemzzy is not None:
            xbmc.log("Nemzzy : $s" % nemzzy, xbmc.LOGINFO)
            if not DEBUG:
                elem.remove(nemzzy)
                os.rename(addonxml,addonxml+'.bak')
                file.write(addonxml)
                msg += 'Removed :\tnemzzy dependancy from %s \n' % addon
            else:
                msg += 'Removed (simulated) :\tnemzzy dependancy from %s \n' % addon



        # msg ="%s version %s was written for %s version %s\n" % (THISNAME,THISVERSN, TRGTNAME, xxxodus_version )
        #
        # msg+="You have %s version %s which is %s\n" % (TRGTNAME, TRGTVER, AGETXT)
        # if older :
        #     msg+="You could try updating %s %s\n"  % (TRGTNAME, TRGTVER )
        # else:
        #     msg+="You could try updating %s\n"  % THISNAME
        # msg+="If that doesnt work try making contact on GitHub\n"
        #
        #
        # window = TextBox(Message=msg)
        # window.doModal()
        # del window


def main():
    global msg,err
    addonxml = requests.get(streamarmyxml).text
    tree = ET.ElementTree(ET.fromstring(addonxml))
    root = tree.getroot()
    addons = list(root.iter("addon"))
    x=0
    for i in addons:
        addon=i.get('id')
        if addon != THISID:
            runpatch(addon)
    if msg.strip()== "":
        msg=err
    window = TextBox(Message=msg)
    window.doModal()
    del window


main()
