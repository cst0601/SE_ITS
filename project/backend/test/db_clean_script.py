from pymongo import MongoClient
client = MongoClient("mongodb://127.0.0.1:27017")
its = client.its

# its.issue_history.delete_many({"issue_id": {"$in" : issueIds}})
# its.comment.delete_many({"issue_id": {"$in" : issueIds}})
# its.issue.delete_many({"project_id": projectId})
# its.project_member.delete_many({"project_id": project_id})
its.project.delete_many({"project_name": {"$in": ["ut_project2", "ut_project"]}})
