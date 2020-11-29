from .. import mongo


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
    return mongo.db.users.distinct("accounts.{}.passwords".format(account))


def getPasswordCount(account):
    return mongo.db.users.distinct("accounts.{}.total_passwords".format(account))


def getPassword(account, id):
    return mongo.db.users.distinct("accounts.{}.passwords.{}".format(account, id))[0]


def pushPassword(account, password):
    mongo.db.users.update(
        {"accounts.{}.passwords".format(account): {"$exists": "true"}},
        {
            "$inc": {"accounts.{}.total_passwords".format(account): 1},
            "$push": {"accounts.{}.passwords".format(account): password}
        }
    )


def updatePassword(account, id, password):
    updated_values = {
        "accounts.{}.passwords.$.{}.website".format(account, id): password["website"],
        "accounts.{}.passwords.$.{}.icon".format(account, id): password["icon"],
        "accounts.{}.passwords.$.{}.username".format(account, id): password["username"],
        "accounts.{}.passwords.$.{}.encrypted".format(account, id): password["encrypted"],
        "accounts.{}.passwords.$.{}.modified".format(account, id): password["modified"],
        "accounts.{}.passwords.$.{}.validURL".format(account, id): password["validURL"],

    }
    mongo.db.users.update(
        {"accounts.{}.passwords.{}".format(account, id): {"$exists": "true"}},
        {'$set': updated_values}
    )


def deletePassword(account, id):
    mongo.db.users.update(
        {"accounts.{}.passwords.{}".format(account,id): {"$exists": "true"}},
        {"$unset": {"accounts.{}.passwords.$".format(account):{"$exists":"true"}}}
    )
    mongo.db.users.update(
        {"accounts.{}.passwords".format(account): {"$exists": "true"}},
        {"$pull": {"accounts.{}.passwords".format(account): None}}
    )
