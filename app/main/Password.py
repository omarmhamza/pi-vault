from .. import hashids
from datetime import datetime


class Password:
    def __init__(self, website, username,icon,_id,raw):
        self.id = hashids.encode(_id)
        self.encrypted = Password.encrypt(raw)
        self.website = website
        self.username = username
        now = datetime.now()
        self.created = now.strftime("%d/%m/%Y, %H:%M:%S")
        self.modified = ""
        if icon:
            self.icon_unicode = icon
        else:
            self.icon_unicode = "0"

    @staticmethod
    def encrypt(raw):
        return "{}{}".format("ency",raw)

    @staticmethod
    def decrypt(encrypted):
        return encrypted

    def jsonifyResponse(self):
        response = vars(self)
        print response
        return response

