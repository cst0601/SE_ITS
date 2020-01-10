from flask_pymongo import PyMongo
from flask import request
mongo = PyMongo()
def getProjectId(username, project_name):
    project_ids = list(mongo.db.project_member.aggregate([
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
        "$match": {"owner_project.project_name": project_name}
    },
    {
        "$unwind": "$owner_project"
    },
    {
        "$project": {"project_id": "$owner_project._id"}
    }
    ]))
    if project_ids == []:
        return None
    return project_ids[0]["project_id"]

def getIssueList(project_id):
    issues = list(mongo.db.issue.aggregate([
    {
        "$match":{"project_id": project_id}
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

def isOwner(cookies, username):
    id = cookies.get('id')
    session = cookies.get('session')
    if id and session:
        currentUser = mongo.db.session.find_one({"id": id, "session": session})
    if currentUser["id"] == username:
        return True
    return False

def isManager(cookies, project_id):
    id = cookies.get('id')
    session = cookies.get('session')
    currentUser = None
    if id and session:
        currentUser = mongo.db.session.find_one({"id": id, "session": session})
    if currentUser == None:
        return False
    result = mongo.db.project_member.find_one({ "project_id": project_id,
                                                "username": currentUser["id"]})
    return result["manager"]
