from pymongo import MongoClient
client = MongoClient("mongodb://127.0.0.1:27017")
its = client.its
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
