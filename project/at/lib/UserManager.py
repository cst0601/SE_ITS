from pymongo import MongoClient
from robot.api.deco import keyword

client = MongoClient("mongodb://127.0.0.1:27017")
its = client.its

class UserManager():
    def __init__(self):
        ROBOT_LIBRARY_SCOPE = "GLOBAL"

    @keyword('Mongo Delete User')
    def delete_user(self, username):
        filter = {"username" : username}
        result = its.user_profile.find_one({"username": username})
        if not result == None:
            its.user_profile.delete_many(filter)

    @keyword("Mongo Create User")
    def create_user(self, username, password, name, email, role="user", lineID=""):
        data= {
            "username": username,
            "password": password,
            "name": name,
            "email": email,
            "role": role,
            "lineID": lineID
        }
        result = its.user_profile.find_one({"username": username})
        if result == None:
            its.user_profile.insert_one(data)
