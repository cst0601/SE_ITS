from functools import wraps
from flask import session, request, redirect, url_for
from .mongo import mongo
from .project import Project
class LoginVerification:
    def login_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id = request.cookies.get('id')
            session = request.cookies.get('session')
            if id and session:
                result = mongo.db.session.find_one({"id": id, "session": session})
                if not result is None:
                    return func(*args, **kwargs)
            return {"info": "redirect",
                    "location": "/sign_in"}
        return decorated_function

    def system_manager_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id = request.cookies.get('id')
            result = mongo.db.user_profile.find_one({"username": id})
            if result["role"] == "manager":
                return func(*args, **kwargs)
            return {"info": "failure",
                    "payload": "Premissin denied."}
        return decorated_function

    def project_member_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id = request.cookies.get('id')
            try:
                projectId = Project(request.get_json()["username"], request.get_json()["project_name"]).projectId
            except:
                return redirect(404)
            result = mongo.db.project_member.find_one({"project_id": projectId, "username": id})
            if result is None:
                return {"info": "redirect",
                        "location": "/404"}
            return func(*args, **kwargs)
        return decorated_function

    def project_owner_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id = request.cookies.get('id')
            try:
                projectId = Project(request.get_json()["username"], request.get_json()["project_name"]).projectId
            except:
                return redirect(404)
            result = mongo.db.project_member.find_one({"project_id": projectId, "username": id, "owner": True})
            if result is None:
                return {"info": "failure",
                        "payload": "Request invalid"}
            return func(*args, **kwargs)
        return decorated_function

    def project_manager_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id = request.cookies.get('id')
            try:
                projectId = Project(request.get_json()["username"], request.get_json()["project_name"]).projectId
            except:
                return redirect(404)
            result = mongo.db.project_member.find_one({"project_id": projectId, "username": id, "$or": [{"owner": True}, {"manager": True}]})
            if result is None:
                return {"info": "failure",
                        "payload": "Request invalid"}
            return func(*args, **kwargs)
        return decorated_function

    def account_owner_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id = request.cookies.get('id')
            username = request.get_json()["username"]

            if not id == username:
                return {"info": "failure",
                        "payload": "Request invalid"}
            return func(*args, **kwargs)
        return decorated_function
