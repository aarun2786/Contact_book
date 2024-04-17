from pymongo import MongoClient
import os
from file_manager import paths
from bson import ObjectId
client = MongoClient("mongodb://localhost:27017/contract_app")
db = client["Contact_book"]
contact = db["Contact"]


def delete_old_photo(id):
    old_photo = contact.find_one({"_id":ObjectId(id)},{'_id':0,"Photo":1})
    os.remove(f"{paths}/{old_photo['Photo']}")
