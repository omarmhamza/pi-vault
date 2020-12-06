from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class Account:
    def __init__(self, username="", password="", facial_img=""):
        self.username = username.lower()
        self.authentication = {
            "hashed": generate_password_hash(password),
            "face": ""
        }
        now = datetime.now()
        date = now.strftime("%d/%m/%Y, %H:%M:%S")
        self.created = str(date)
        self.passwords = []
        self.total_passwords = 0
        self._id = str(uuid.uuid4().fields[-1])[:5]
        self.active = self.authenticated = self.anonymous = False

    def authenticate(self):
        self.active = self.authenticated = True

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return int(self._id)

    @staticmethod
    def load_account(user):
        account = Account(username=user["username"])
        account._id = user["_id"]
        return account

    @staticmethod
    def check_password(hashed, raw):
        return check_password_hash(hashed, raw)

    @staticmethod
    def check_facial(stored_image, captured):
        pass

    def jsonify(self):
        dataFrame = vars(self).copy()
        del dataFrame["authenticated"]
        del dataFrame["anonymous"]
        del dataFrame["active"]
        response = dataFrame
        return response

    @property
    def id(self):
        return self._id

