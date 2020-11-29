from .. import hashids
from datetime import datetime


class Password:
    def __init__(self, website, username,icon,raw,_id):
        self.encrypted = Password.encrypt(raw)
        self.website = website
        self.username = username
        now = datetime.now()
        date = now.strftime("%d/%m/%Y, %H:%M:%S")
        self.created = date
        self._id = hashids.encode(_id)
        if icon:
            self.icon_unicode = icon
        else:
            self.icon_unicode = "f084" #key icon font awesome

    @staticmethod
    def encrypt(raw):
        return "{}{}".format("ency",raw)

    @staticmethod
    def decrypt(encrypted):
        return encrypted

    def jsonifyResponse(self):
        dataFrame = vars(self).copy()
        del dataFrame["_id"]
        response = {str(self._id):dataFrame}
        return response


