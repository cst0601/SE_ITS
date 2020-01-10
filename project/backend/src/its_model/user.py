from pymongo import MongoClient
from .project import Project
client = MongoClient("mongodb://127.0.0.1:27017")
its = client.its
class ItsUser:
    def __init__(self, username):
        self.username = username

    def getProfile(self, username = None):
        if username == None:
            username = self.username
        profile = its.user_profile.find_one({"username": username}, {
            "_id": 0,
            "username": 1,
            "email": 1,
            "name": 1,
            "lineID": 1})
        if profile == None:
            raise Exception("User not found.")
        profile["isOwner"] = self.username == username
        return profile

    def updateProfile(self, newProfile):
        query = {"username": self.username}
        newValues = { "$set": {"email": newProfile["email"],
                                "lineID": newProfile["lineID"],
                                "name": newProfile["name"] } }
        its.user_profile.update_one(query, newValues)

    def updatePassword(self, oldPassword, newPassword):
        result = its.user_profile.find_one({"username": self.username,
                                            "password": oldPassword})
        if result is None:
            raise Exception("Password error")
        query = {"username": self.username}
        newValues = { "$set": { "password": newPassword}}
        its.user_profile.update_one(query, newValues)

    def isPasswordCorrect(self, password):
        result = its.user_profile.find_one({"username": self.username,
                                            "password": password})
        if result is None:
            return False
        return True

    def getProjectList(self):
        """ will return
                [{username: <projectId>,
                 project_name: <projectName>}, ...]"""
        projects = list(its.project_member.aggregate([
        {
            "$match":{"username": self.username}
        },
        {
            "$lookup":
            {
              "from": "project",
              "localField": "project_id",
              "foreignField": "_id",
              "as": "selected_project"
            }
        },
        {
            "$unwind": "$selected_project"
        },
        {
            "$lookup":
            {
              "from": "project_member",
              "localField": "project_id",
              "foreignField": "project_id",
              "as": "selected_project_member"
            }
        },
        {
            "$unwind": "$selected_project_member"
        },
        {
            "$match": {"selected_project_member.owner": True}
        },
        {
            "$project": {"username": "$selected_project_member.username", "project_name": "$selected_project.project_name", "_id": 0}
        }
        ]))
        return projects

    def getOwnerProjects(self):
        """ will return
                [{project_id: <projectId>,
                 project_name: <projectName>}, ...]"""
        return list(its.project_member.aggregate([
        {
            "$match":{"username": self.username, "owner": True}
        },{
            "$lookup":{
              "from": "project",
              "localField": "project_id",
              "foreignField": "_id",
              "as": "project"
            }
        },
        {
            "$unwind": "$project"
        },
        {
            "$project": {"project_id": "$project_id", "project_name": "$project.project_name", "_id": 0}
        }
        ]))

    def createProject(self, projectName):
        if projectName in [project["project_name"] for project in self.getOwnerProjects()]:
            raise Exception("Project name is exist.")

        insertedResult = its.project.insert_one({"project_name": projectName, "description": ""})
        its.project_member.insert_one({
            "project_id": insertedResult.inserted_id,
            "username": self.username,
            "owner": True,
            "manager" : True,
            "tester": False,
            "developer": False
        })

    def getProjectId(self, projectName):
        for project in self.getOwnerProjects():
            if project["project_name"] == projectName:
                return project["project_id"]
        raise Exception("Project not exist.")

    def deleteProject(self, projectName):
        try:
            project = Project(self.username, projectName)
        except:
            raise Exception("Project not exist.")
        project.deleteIssue()
        its.project_member.delete_many({"project_id": project_id})
        its.project.delete_one({"_id": project_id})
