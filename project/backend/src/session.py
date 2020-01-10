"""
session.py
Create and validate login session.
"""
import hashlib
import datetime
from .its_model.mongo import mongo

# Generates a login session
# - Saves a session entity to DB ["_id", "hashCode"]
# - Returns session hash code
def generateSession(id, username):
    md5 = hashlib.md5()
    data = id + \
           username + \
           str(datetime.datetime.now())
    md5.update(data.encode("utf-8"))
    hashCode = md5.hexdigest()

    # PyMongo will automantically add _id field if not included
    # userId servers as key, type of string
    mongo.db.session.replace_one(filter={"_id": id},
        replacement={"_id": id, "hashCode": hashCode},
        upsert=True)

    return hashCode

def generateHashFileName(filename):
    extension = filename.split('.')[-1]
    md5 = hashlib.md5()
    data = filename + \
           str(datetime.datetime.now())
    md5.update(data.encode("utf-8"))
    hashCode = md5.hexdigest()
    return hashCode + "." + extension

# Validate if the session is legal
def validateSession(id, sessionHashCode):
    storedHash = mongo.db.session.find_one({"_id": id})
    if storedHash is sessionHashCode:
        return True;
    return False
