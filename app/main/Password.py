from .. import hashids
from datetime import datetime
import re


class Password:
    def __init__(self, website, username, icon, raw, _id):
        self.encrypted = Password.encrypt(raw)
        self.website = website
        self.username = username
        self.validURL = True if self.validateURL(website) else False
        now = datetime.now()
        date = now.strftime("%d/%m/%Y, %H:%M:%S")
        self.created = date
        self._id = hashids.encode(_id)
        if icon:
            self.icon = icon
        else:
            self.icon = {"unicode": "f084"}

    @staticmethod
    def encrypt(raw):
        return "{}{}".format("ency", raw)

    @staticmethod
    def decrypt(encrypted):
        return encrypted

    @staticmethod
    def validateURL(url):
        regex = re.compile(
            # r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, str(url)) is not None

    def jsonifyResponse(self):
        dataFrame = vars(self).copy()
        del dataFrame["_id"]
        response = {str(self._id): dataFrame}
        return response
