from datetime import datetime
import re
from cryptography.fernet import Fernet
import shortuuid


def create_key():
    key = Fernet.generate_key().decode("utf-8")
    f = open("../secret.key","w")
    f.write(key)
    f.close()


def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()


class Encryption:
    @staticmethod
    def encrypt(raw):
        key = load_key()
        encoded_message = raw.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)
        return str(encrypted_message.decode("utf-8"))

    @staticmethod
    def decrypt(encrypted):
        key = load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(bytes(encrypted,encoding='utf8'))
        return decrypted_message.decode()


class Password:
    def __init__(self, website, username, icon, raw, _id):
        self.encrypted = Encryption.encrypt(raw)
        if "http://" in website:
            self.website = str(website.strip("http://"))
        elif "https://" in website:
            self.website = str(website.strip("https://"))
        else:
            self.website = str(website)
        self.website = Encryption.encrypt(self.website)
        self.username = Encryption.encrypt(username)
        self.validURL = True if self.validateURL(website) else False
        self.modified = ""
        now = datetime.now()
        date = now.strftime("%d/%m/%Y, %H:%M:%S")
        self.created = date
        self._id = shortuuid.uuid()
        if icon:
            self.icon = icon
        else:
            self.icon = {"unicode": "f084"}

    @staticmethod
    def validateURL(url):
        regex = re.compile(
            '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$',
            re.IGNORECASE)
        return re.match(regex, str(url)) is not None

    # @staticmethod
    # def encryptAll(dataFrame):
    #     for key in dataFrame:
    #         if isinstance(dataFrame[key], str):
    #             dataFrame[key] = Encryption.encrypt(dataFrame[key])
    #     return dataFrame
    #
    # @staticmethod
    # def decryptAll(dataFrame):
    #     for key in dataFrame:
    #         try:
    #             dataFrame[key] = Encryption.decrypt(dataFrame[key])
    #         except:
    #             pass
    #     return dataFrame

    def jsonifyResponse(self):
        dataFrame = vars(self).copy()
        del dataFrame["_id"]
        # dataFrame = self.encryptAll(dataFrame)
        response = {str(self._id): dataFrame}
        return response
