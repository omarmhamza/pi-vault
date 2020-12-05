from .. import mongo
from Password import Encryption
from .. import login_manager


def getIcons():
    icons = []
    get_icons = mongo.db.icons.find()
    for icon in get_icons:
        coded = "{}{}".format("&#x", icon["unicode"])
        icons.append((coded, icon["name"]))
    return icons


def getIconFromList(value):
    icon_selected = str(value.pop().decode('utf-8')).strip("&#x")
    icon = mongo.db.icons.find_one({"unicode": icon_selected})
    return icon


def getPasswords(account):
    return mongo.db.users.distinct("{}.passwords".format(account))


def getPasswordCount(account):
    search = mongo.db.users.distinct("{}.total_passwords".format(account))
    if search:
        return search[0]
    else:
        return None


def getPassword(account, id):
    search = mongo.db.users.distinct("{}.passwords.{}".format(account, id))
    if search:
        password = search[0]
        password["encrypted"] = Encryption.decrypt(password["encrypted"])
        password["username"] = Encryption.decrypt(password["username"])
        password["website"] = Encryption.decrypt(password["website"])
        return password
    else:
        return None


def pushPassword(account, password):
    mongo.db.users.update(
        {"{}.passwords".format(account): {"$exists": "true"}},
        {
            "$inc": {"{}.total_passwords".format(account): 1},
            "$push": {"{}.passwords".format(account): password}
        }
    )


def updatePassword(account, id, password):
    updated_values = {
        "{}.passwords.$.{}.website".format(account, id): password["website"],
        "{}.passwords.$.{}.icon".format(account, id): password["icon"],
        "{}.passwords.$.{}.username".format(account, id): password["username"],
        "{}.passwords.$.{}.encrypted".format(account, id): password["encrypted"],
        "{}.passwords.$.{}.modified".format(account, id): password["modified"],
        "{}.passwords.$.{}.validURL".format(account, id): password["validURL"],

    }
    mongo.db.users.update(
        {"{}.passwords.{}".format(account, id): {"$exists": "true"}},
        {'$set': updated_values}
    )


def deletePassword(account, id):
    mongo.db.users.update(
        {"{}.passwords.{}".format(account, id): {"$exists": "true"}},
        {"$unset": {"{}.passwords.$".format(account): {"$exists": "true"}}}
    )
    mongo.db.users.update(
        {"{}.passwords".format(account): {"$exists": "true"}},
        {
            "$inc": {"{}.total_passwords".format(account): -1},
            "$pull": {"{}.passwords".format(account): None}
        }
    )


def addAccount(account):
    mongo.db.users.insert(account.jsonify())


def getAccountId(username):
    search = mongo.db.users.distinct("{}".format(username))
    if search:
        return search[0]
    else:
        return None


def validateAccount(username, raw_password):
    search = mongo.db.users.distinct("{}".format(username))
    if search:
        return search[0]
    else:
        return None


@login_manager.user_loader
def load_user(username):
    return getAccountId(username)
