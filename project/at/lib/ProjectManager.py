from pymongo import MongoClient
from robot.api.deco import keyword
import datetime
client = MongoClient("mongodb://127.0.0.1:27017")
its = client.its

class ProjectManager:
    def __init__(self):
        ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def getOwnerProjects(self, username):
        return list(its.project_member.aggregate([
        {
            "$match":{"username": username, "owner": True}
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

    def getProjectId(self, username, projectName):
        for project in self.getOwnerProjects(username):
            if project["project_name"] == projectName:
                return project["project_id"]
        raise Exception("Project not exist.")

    @keyword('Mongo Delete Project')
    def deleteProject(self, owner, projectName):
        try:
            project_id = self.getProjectId(owner, projectName)
        except:
            raise Exception("Project not exist.")
        issues =  list(its.issue.find({"project_id": project_id}, {"_id": 1}))
        issueIds = [issue["_id"] for issue in issues]
        its.issue_history.delete_many({"issue_id": {"$in" : issueIds}})
        its.comment.delete_many({"issue_id": {"$in" : issueIds}})
        its.issue.delete_many({"project_id": project_id})
        its.project_member.delete_many({"project_id": project_id})
        its.project.delete_one({"_id": project_id})

    @keyword('Mongo Create Project')
    def createProject(self, username, projectName):
        insertedResult = its.project.insert_one({"project_name": projectName, "description": ""})
        its.project_member.insert_one({"project_id": insertedResult.inserted_id, "username": username, "owner": True, "manager" : True})

    @keyword('Mongo Delete Project Member')
    def deleteProjectMember(self, owner, username, projectName):
        project_id = self.getProjectId(owner, projectName)
        its.project_member.delete_one({
        "project_id": project_id,
        "username": username,
        })

    @keyword('Mongo Add Project Member')
    def addProjectMember(self, owner, username, projectName):
        project_id = self.getProjectId(owner, projectName)
        its.project_member.insert_one({
        "project_id": project_id,
        "username": username,
        "owner": False,
        "Manager": False
        })

    @keyword('Mongo Delete Issue')
    def deleteIssue(self, owner, projectName, issueNumber):
        projectId = self.getProjectId(owner, projectName)
        selectedIssues = list(its.issue.find(filter))
        for issue in selectedIssues:
            its.comment.delete_many({"issue_id": issue["_id"]})
            its.issue_history.delete_many({"issue_id": issue["_id"]})
            its.issue.delete_one({"project_id": projectId, "issue_number": issueNumber})

    def getLastIssueId(self, owner, projectName):
        projectId = self.getProjectId(owner, projectName)
        lastIssue = its.issue.find_one({"$query": {"project_id": projectId}, "$orderby": {"issue_number": -1}})
        new_issue_number = 1
        if lastIssue != None:
            new_issue_number = lastIssue["issue_number"] + 1
        return new_issue_number

    @keyword('Mongo Create Issue')
    def createIssue(self, owner, creator, projectName, title="", comment="", state="open"):
        newIssueNumber = self.getLastIssueId(owner, projectName)
        projectId = self.getProjectId(owner, projectName)
        its.issue.insert_one({
            "project_id": projectId,
            "issue_number": newIssueNumber,
            "title": title,
            "severity": "",
            "priority": "",
            "reproducible": "",
            "assignees": [],
            "comment": comment,
            "state": state,
            "date": datetime.datetime.utcnow(),
            "creator": creator
        })

    #單獨執行可以新增，robot使用會失敗
    @keyword('Mongo Add Assignees')
    def addAssignee(self, issueNumber, assignees):
        myquery = {"issue_number": int(issueNumber)}
        assigneesList = [assignees]
        newValues = {"$set": {"assignees": assigneesList}}
        its.issue.update_one(myquery, newValues)
