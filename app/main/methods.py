from .. import mongo
from .Password import Encryption
from .. import login_manager
from werkzeug.security import generate_password_hash


def getIcons():
    icons = []
    get_icons = mongo.db.icons.find()
    for icon in get_icons:
        coded = "{}{}".format("&#x", icon["unicode"])
        icons.append((coded, icon["name"]))
    return icons


def getIconFromList(value):
    print(value)
    icon_selected = str(value.pop()).strip("&#x")
    icon = mongo.db.icons.find_one({"unicode": icon_selected})
    return icon


def getPasswords(account_id):
    return mongo.db.users.find_one({"_id": "{}".format(account_id)})["passwords"]


def getPasswordCount(account):
    search = mongo.db.users.distinct("{}.total_passwords".format(account))
    if search:
        return search[0]
    else:
        return None


def getPassword(account_id, pass_id):
    search = mongo.db.users.distinct("passwords.{}".format(pass_id), {"_id": "{}".format(account_id)})[0]
    if search:
        password = search
        password["encrypted"] = Encryption.decrypt(search["encrypted"])
        password["username"] = Encryption.decrypt(search["username"])
        password["website"] = Encryption.decrypt(search["website"])
        return password
    else:
        return None


def pushPassword(id, password):
    mongo.db.users.update(
        {"_id": "{}".format(id)},
        {
            "$inc": {"total_passwords": 1},
            "$push": {"passwords": password}
        }
    )


def updatePassword(account_id, pass_id, password):
    updated_values = {
        "passwords.$.{}.website".format(pass_id): password["website"],
        "passwords.$.{}.icon".format(pass_id): password["icon"],
        "passwords.$.{}.username".format(pass_id): password["username"],
        "passwords.$.{}.encrypted".format(pass_id): password["encrypted"],
        "passwords.$.{}.modified".format(pass_id): password["modified"],
        "passwords.$.{}.validURL".format(pass_id): password["validURL"],

    }
    mongo.db.users.update(
        {"_id": "{}".format(account_id), "passwords.{}".format(pass_id): {"$exists": "true"}},
        {'$set': updated_values}
    )


def deletePassword(account_id, pass_id):
    mongo.db.users.update(
        {"_id": "{}".format(account_id), "passwords.{}".format(pass_id): {"$exists": "true"}},
        {"$unset": {"passwords.$": {"$exists": "true"}}}
    )
    mongo.db.users.update(
        {"_id": "{}".format(account_id)},
        {
            "$inc": {"total_passwords": -1},
            "$pull": {"passwords": None}
        }
    )


def addAccount(account):
    mongo.db.users.insert(account.jsonify())


def updateCredentials(user_id, username, password):
    mongo.db.users.update(
        {"_id": "{}".format(user_id)},
        {"$set": {
            "username": str(username),
            "authentication.hashed": generate_password_hash(str(password))
        }
        }
    )


def checkAvailability(username):
    if username:
        search = mongo.db.users.find_one({"username": "{}".format(username)})
        if search:
            return False
        else:
            return True
    return None


def getAccountById(id):
    search = mongo.db.users.find_one({"_id": "{}".format(id)})
    if search:
        return search
    else:
        return None


def validateAccount(username):
    search = mongo.db.users.find_one({"username": "{}".format(username)})
    if search:
        return search
    else:
        return None


@login_manager.user_loader
def load_user(id):
    from .Account import Account
    user = getAccountById(id)
    return Account.load_account(user)
