from pymongo import MongoClient
import datetime
from .issue import Issue
client = MongoClient("mongodb://127.0.0.1:27017")
its = client.its
class Project:
    def __init__(self, username, projectName):
        project_ids = list(its.project_member.aggregate([
        {
            "$match":{"owner": True, "username": username}
        },{
            "$lookup":{
              "from": "project",
              "localField": "project_id",
              "foreignField": "_id",
              "as": "owner_project"
            }
        },
        {
            "$match": {"owner_project.project_name": projectName}
        },
        {
            "$unwind": "$owner_project"
        },
        {
            "$project": {"project_id": "$owner_project._id"}
        }
        ]))
        if project_ids == []:
            raise Exception("Project not exist.")
        self.projectId = project_ids[0]["project_id"]

    def getData(self):
        result = its.project.find_one({"_id":self.projectId}, {
            "project_name": 1,
            "description": 1,
            "_id": 0
        })
        return result

    def updateDescription(self, description):
        its.project.update_one({"_id": self.projectId}, {"$set": {"description": description}})

    def getMemberList(self):
        return list(its.project_member.aggregate([
        {
            "$match":{"project_id": self.projectId}
        },
        {
            "$lookup":
            {
              "from": "user_profile",
              "localField": "username",
              "foreignField": "username",
              "as": "selected_user"
            }
        },
        {
            "$unwind": "$selected_user"
        },
        {
            "$project": {
                            "_id": 0,
                            "username": 1,
                            "owner": 1,
                            "manager": 1,
                            "developer": 1,
                            "tester": 1,
                            "name": "$selected_user.name",
                            "email": "$selected_user.email"
                        }
        }
        ]))
    def isManager(self, username):
        roleOfProject = its.project_member.find_one({ "project_id": self.projectId,
                                                      "username": username})
        if roleOfProject["owner"] or roleOfProject["manager"]:
            return True
        return False

    def removeMember(self, username):
        try:
            its.project_member.delete_one({"project_id": self.projectId, "username": username})
        except:
            raise Exception("Project member not exist.")
        its.issue.update_many({"project_id": self.projectId}, {"$pull": {"assignees": username}})

    def getIssue(self, issueNumber):
        try:
            issue = Issue(self.projectId, issueNumber)
        except:
            raise Exception("Issue not exist.")
        return issue

    def getIssueList(self):
        issues = list(mongo.db.issue.aggregate([
        {
            "$match":{"project_id": self.projectId}
        },{
            "$lookup":{
              "from": "comment",
              "localField": "_id",
              "foreignField": "issue_id",
              "as": "comments"
             }
        },{
            "$addFields": {
                "comment_amount":{
                    "$size": "$comments"
                }
            }
        },{
            "$lookup":{
              "from": "issue_history",
              "localField": "_id",
              "foreignField": "issue_id",
              "as": "historys"
             }
        },{
            "$addFields": {
                "comments":{
                    "$concatArrays": ["$comments", "$historys"]
                }
            }
        },{
            "$addFields": {
                "last_update_time":{
                    "$max": [{"$max": "$comments.date"},"$date"]
                }
            }
        },{
            "$project": {
                "_id": 0,
                "project_id": 0,
                "comments": 0,
                "historys": 0
            }
        }
        ]))
        return issues

    def getLastIssueId(self):
        lastIssue = its.issue.find_one({"$query": {"project_id": self.projectId}, "$orderby": {"issue_number": -1}})
        new_issue_number = 1
        if lastIssue != None:
            new_issue_number = lastIssue["issue_number"] + 1
        return new_issue_number

    def createIssue(self, creator, issueData):
        newIssueNumber = self.getLastIssueId()
        its.issue.insert_one({
            "project_id": self.projectId,
            "issue_number": newIssueNumber,
            "title": issueData["title"],
            "severity": issueData["severity"],
            "priority": issueData["priority"],
            "reproducible": issueData["reproducible"],
            "assignees": issueData["assignees"],
            "comment": issueData["comment"],
            "state": "open",
            "date": datetime.datetime.utcnow(),
            "creator": creator
        })
        return newIssueNumber

    def deleteIssue(self, filter = {}):
        filter["project_id"] = self.projectId
        selectedIssues = list(its.issue.find(filter))
        selectedIssueIds = [issue["_id"] for issue in selectedIssues]
        its.issue_history.delete_many({"issue_id": {"$in" : selectedIssueIds}})
        its.comment.delete_many({"issue_id": {"$in" : selectedIssueIds}})
        its.issue.delete_many({"_id": selectedIssueIds})

    def updateMemberRole(self, memberUsername, roleDict):
        myquery = {"project_id": self.projectId, "username": memberUsername}
        newValue = {"$set": {roleDict["role"]: roleDict["value"]}}
        print(newValue)
        try:
            its.project_member.update_one(myquery, newValue)
        except:
            raise Exception("Member not exist.")

    def addNewMember(self, memberInfoDict):
        result = its.project_member.find_one({"project_id": self.projectId,
                                                  "username": memberInfoDict["username"]})
        member = its.user_profile.find_one({"username": memberInfoDict["username"]})
        if (result is not None) or (member is None):
            raise Exception("Member is not exist or has been added to this project.")
        memberInfoDict["project_id"] = self.projectId
        memberInfoDict["owner"] = False
        its.project_member.insert_one(memberInfoDict)
