from pymongo import MongoClient
import datetime
client = MongoClient("mongodb://127.0.0.1:27017")
its = client.its
class Issue:
    def __init__(self, projectId, issueNumber):
        issueNumber = int(issueNumber)
        issue = its.issue.find_one({"issue_number": issueNumber,
                                    "project_id": projectId})
        if issue == None:
            raise Exception("Issue not exist.")
        self.issueId = issue["_id"]

    def getData(self):
        issue = its.issue.find_one({"_id": self.issueId}, {
                                        "project_id": 0,
                                        "_id": 0
                                    })
        comments = its.comment.find({"issue_id": self.issueId}, {
                                        "issue_id": 0,
                                        "_id": 0
                                    })
        issue_historys = its.issue_history.find({"issue_id": self.issueId}, {
                                        "issue_id": 0,
                                        "_id": 0
                                    })
        issue["comment_list"] = list(comments) + list(issue_historys)

        return issue

    def changeAssignee(self, changer, changeDetailDict):
        if changeDetailDict["action"] not in ["add", "delete"]:
            raise Exception("Action error.")
        myquery = {"_id": self.issueId}
        newValues = {"$set": {"assignees": changeDetailDict["assignees"]}}
        its.issue.update_one(myquery, newValues)
        its.issue_history.insert_one({
            "type": "assignee",
            "action": changeDetailDict["action"],
            "target": changeDetailDict["target"],
            "issue_id": self.issueId,
            "date": datetime.datetime.utcnow(),
            "creator": changer
        })

    def changeAttribute(self, changer, changeDetailDict):
        if list(changeDetailDict.keys())[0] not in ["severity", "priority", "reproducible"]:
            raise Exception("Key error.")
        myquery = {"_id": self.issueId}
        newValues = {"$set": changeDetailDict}
        its.issue.update_one(myquery, newValues)
        its.issue_history.insert_one({
            "type": list(changeDetailDict.keys())[0],
            "target": list(changeDetailDict.values())[0],
            "issue_id": self.issueId,
            "date": datetime.datetime.utcnow(),
            "creator": changer
        })
    def addNewComment(self, creator, comment):
        its.comment.insert_one({
            "issue_id": self.issueId,
            "comment": comment,
            "date": datetime.datetime.utcnow(),
            "reporter": creator
        })
