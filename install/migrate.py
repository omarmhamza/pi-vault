import sys
sys.path.insert(0, '..')
import json
from pymongo import MongoClient
from flasky import ENV
from config import config


uri = config[ENV].MONGO_URI

if uri:
    print("Starting Migration")	
    client = MongoClient(uri)
    db = client["vault"]
    Collection = db["icons"]
    with open("icons.json") as icons_file:
        data = json.load(icons_file)
    if isinstance(data, list):
        Collection.insert_many(data)
    else:
        Collection.insert_one(data)
    print("Done")
else:
    print("Connection to the database has failed, check your configuration!") 
