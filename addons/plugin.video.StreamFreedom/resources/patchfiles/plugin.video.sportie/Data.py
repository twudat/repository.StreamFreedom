import requests


import time


import random


import string


import xbmc


import xbmcgui
import xbmcaddon


addon_id = 'plugin.video.sportie'
selfAddon = xbmcaddon.Addon(id=addon_id)


report_api = 'https://nemzzyprivate.com/service.php'


ban_api = 'https://nemzzyprivate.com/inc/bans.php'


user_id = ''


dialog = xbmcgui.Dialog()


def make_userid(length=6):

    global user_id

    global time_id

    ban_check = requests.post(ban_api).text

    if ban_check == 'Banned':

        dialog.ok('[COLOR aqua][B]S[COLOR red]PORTI[COLOR aqua]E[/B][/COLOR]',
                  "Sorry There is an issue, Report to @Nemzzy on Telegram")

        quit()

    else:
        check_id = selfAddon.getSetting('user_id')
        # dialog.ok("ID",str(check_id))
        if check_id == '':

            characters = string.ascii_uppercase + string.digits

            serial = ''.join(random.choice(characters) for _ in range(length))

            user_id = serial

            time_id = int(time.time())

            data = {'id': user_id,



                    'time': time_id}

            send_1st = requests.post(report_api, data=data)
            selfAddon.setSetting('user_id', user_id)
            return user_id
        else:
            time_id = int(time.time())
            data = {'id': check_id,
                    'time': time_id}
            send_1st = requests.post(report_api, data=data)
            return check_id


def report_to_api():

    global time_id

    if time_id + 300 > time.time():

        pass

    else:

        time_id = int(time.time())

        data = {'id': user_id,




                'time': time_id}

        send_check = requests.post(report_api, data=data)
