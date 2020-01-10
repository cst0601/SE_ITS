from flask_pymongo import PyMongo
from flask import request
MONGO_URI = "mongodb://127.0.0.1:27017/its"
mongo = PyMongo()

def createRoot():
    from pymongo import MongoClient
    from pymongo.uri_parser import parse_uri
    client = MongoClient(MONGO_URI)
    its = client[parse_uri(MONGO_URI)['database']]
    its.user_profile.insert_one({
        "username":"root",
        "name":"Root",
        "password":"root",
        "email":"root@email",
        "lineID":"root",
        "role":"manager"
    })

if __name__ == "__main__":
    createRoot()
