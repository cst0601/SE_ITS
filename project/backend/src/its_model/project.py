from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from .mongo import MONGO_URI
import datetime
from .issue import Issue
client = MongoClient(MONGO_URI)
its = client[parse_uri(MONGO_URI)['database']]
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
        self.projectName = projectName

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
        """ format of return: {
                "username": <username>,
                "owner": [True|False],
                "manager": [True|False],
                "tester": [True|False],
                "developer": [True|False]
                'name': <name_of_user>,
                'email': <email_of_user>}    """
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
        result = its.project_member.delete_one({"project_id": self.projectId, "username": username})
        if result.deleted_count == 0:
            raise Exception("Project member not exist.")
        its.issue.update_many({"project_id": self.projectId}, {"$pull": {"assignees": username}})

    def getIssue(self, issueNumber):
        try:
            issue = Issue(self.projectId, issueNumber)
        except:
            raise Exception("Issue not exist.")
        return issue

    def getIssueList(self):
        issues = list(its.issue.aggregate([
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
        new_issue_number = 0
        if lastIssue != None:
            new_issue_number = lastIssue["issue_number"]
        return new_issue_number

    def createIssue(self, creator, issueData):
        newIssueNumber = self.getLastIssueId() + 1
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
        its.issue.delete_many({"_id": {"$in" : selectedIssueIds}})

    def updateMemberRole(self, memberUsername, roleDict):
        """ format of memberInfoDict: {
                "role": <roleName>,
                "value": [True|False]}    """
        myquery = {"project_id": self.projectId, "username": memberUsername}
        newValue = {"$set": {roleDict["role"]: roleDict["value"]}}
        result = its.project_member.update_one(myquery, newValue)
        if result.modified_count == 0:
            raise Exception("Member not exist.")

    def addNewMember(self, memberInfoDict):
        """ format of memberInfoDict: {
                "username": <username>,
                "manager": [True|False],
                "tester": [True|False],
                "developer": [True|False]}    """
        result = its.project_member.find_one({"project_id": self.projectId,
                                                  "username": memberInfoDict["username"]})
        member = its.user_profile.find_one({"username": memberInfoDict["username"]})
        if (result is not None) or (member is None):
            raise Exception("Member is not exist or has been added to this project.")
        memberInfoDict["project_id"] = self.projectId
        memberInfoDict["owner"] = False
        its.project_member.insert_one(memberInfoDict)
