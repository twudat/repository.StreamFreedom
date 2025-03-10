# Deobfuscated by StreamFreedom from XXX-O-DUS version="5.00.023"
import xbmc
DEBUG=True

def DLog(message="" ):
    if DEBUG and message!="":
        msg=">>>>>%s" % message
        xbmc.log( msg=msg, level=xbmc.LOGINFO)

