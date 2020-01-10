from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from .mongo import MONGO_URI
client = MongoClient(MONGO_URI)
its = client[parse_uri(MONGO_URI)['database']]
class UserManager:
    def createUser(self, userData):
        result = its.user_profile.find_one({"username": userData["username"]})
        if not result == None:
            raise Exception("Username exists")
        documentKey = ["username", "name", "email", "lineID", "password"]
        document = {}
        for key in documentKey:
            if key in userData.keys():
                document[key] = userData[key]
            else:
                document[key] = ""
        document["role"] = "user"
        its.user_profile.insert_one(document)

    def deleteUser(self, filter):
        its.user_profile.delete_many(filter)

    def getUsers(self):
        return list(its.user_profile.find({}, {"_id": 0,
                                                "username": 1,
                                                "role": 1,
                                                "name": 1,
                                                "email": 1}))

    def updateRole(self, username, role):
        myquery = { "username": username}
        newValue = {"$set": {"role": role}}
        result = its.user_profile.update_one(myquery, newValue)
        if result.matched_count == 0:
            raise Exception("Update fail.")
