# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

from httplib import HTTPSConnection
from urllib import urlencode

import requests
import sickbeard

from sickbeard import logger, common

class HowlEvent(object):
    "Class representing a single Howl event."

    DEFAULT_USER_AGENT = 'PyHowl/0.1'

    def __init__(self, application, name, title, description):
        self.application = application
        self.name = name
        self.title = title
        self.description = description

    @property
    def url(self):
        url = 'https://howlapp.com/public/api/notification'
        return url

    def request(self, username, password, user_agent=DEFAULT_USER_AGENT):
        request = requests.post(self.url,
            auth=(username, password),
            headers={'User-agent': user_agent},
            data={
                'application': self.application,
                'name': self.name,
                'title': self.title,
                'description': self.description,
                'icon-md5': 'dc0f5209059a0e7f3ff298680f98bc1b',
                'icon-sha1': '22339dd6e17eb099ed023c72bd7b5deaf785f2bb',
            }
        )
        return request


class HowlNotifier:

    def test_notify(self, username, password):
        return self._sendHowl(username=username, password=password, event="Test", message="Testing Howl settings from Sick Beard", force=True)

    def notify_snatch(self, ep_name):
        if sickbeard.HOWL_NOTIFY_ONSNATCH:
            self._sendHowl(username=sickbeard.HOWL_USERNAME, password=sickbeard.HOWL_PASSWORD, event=common.notifyStrings[common.NOTIFY_SNATCH], message=ep_name)

    def notify_download(self, ep_name):
        if sickbeard.HOWL_NOTIFY_ONDOWNLOAD:
            self._sendHowl(username=sickbeard.HOWL_USERNAME, password=sickbeard.HOWL_PASSWORD, event=common.notifyStrings[common.NOTIFY_DOWNLOAD], message=ep_name)

    def _sendHowl(self, username=None, password=None, event=None, message=None, force=False):

        if not sickbeard.USE_HOWL and not force:
            return False

        if not username:
            username = sickbeard.HOWL_USERNAME

        if not password:
            password = sickbeard.HOWL_PASSWORD

        application = "Sick Beard Notifier"

        logger.log(u"Howl application: " + application, logger.DEBUG)
        logger.log(u"Howl event: " + event, logger.DEBUG)
        logger.log(u"Howl message: " + message, logger.DEBUG)
        logger.log(u"Howl username: " + username, logger.DEBUG)
        logger.log(u"Howl password: " + password, logger.DEBUG)

        howl_event = HowlEvent(application, event, event, message)
        request = howl_event.request(username, password)

        if request.status_code == 200:
            logger.log(u"Howl notifications sent.", logger.DEBUG)
            return True
        elif request.status_code == 401:
            logger.log(u"Howl auth failed: (invalid username or password)", logger.ERROR)
            return False
        else:
            logger.log(u"Howl notification failed.", logger.ERROR)
            return False


notifier = HowlNotifier
