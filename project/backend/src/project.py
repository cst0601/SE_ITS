from flask import Blueprint, request
from .its_model.mongo import mongo
from .its_model.login_verification import LoginVerification
from .its_model.user import ItsUser
from .its_model.project import Project
from .response import redirect, success, failure

project_bp = Blueprint('project', __name__, url_prefix='/project')
@project_bp.route('/get_project', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def getProjectInfo():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    result = project.getData()
    result["owner"] = request.cookies.get("id") == request.get_json()["username"]
    return success(result)

@project_bp.route('/update_description', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def updateProjectInfo():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    project.updateDescription(request.get_json()["description"])
    return success("Update description succeed.")

@project_bp.route('/list', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.account_owner_required
def getProjectList():
    user = ItsUser(request.cookies.get("id"))
    return success(user.getProjectList())

@project_bp.route('/list/create_project', methods=["POST"])
@LoginVerification.login_required
def createProject():
    username = request.cookies.get('id')
    projectName = request.get_json()["project_name"]
    user = ItsUser(username)
    try:
        user.createProject(projectName)
    except:
        return failure("Project name is exist.")
    return redirect(username + "/" + projectName)

@project_bp.route('/delete_project', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_owner_required
def deleteProject():
    user = ItsUser(request.cookies.get('id'))
    try:
        user.deleteProject(request.get_json()["project_name"])
    except:
        return failure("Project not exist.")
    return success("Delete success.")

@project_bp.route('/member_list', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def getMemberList():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    results = {}
    results["members"] = project.getMemberList()
    results["isManager"] = project.isManager(request.cookies.get('id'))
    return success(results)

@project_bp.route('/remove_member', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_manager_required
def removeMember():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    try:
        project.removeMember(request.get_json()["selected_username"])
    except:
        return failure("Project member not exist.")
    return success({"members": project.getMemberList()})

@project_bp.route('/update_member_role', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_manager_required
def updateMemberRole():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    try:
        project.updateMemberRole(request.get_json()["selected_username"], request.get_json())
    except:
        return failure("Member not exist.")
    return success({"members": project.getMemberList()})

@project_bp.route('/add_new_member', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_manager_required
def addNewMember():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    try:
        project.addNewMember(request.get_json()["new_member_data"])
    except:
        return failure("Member is not exist or has been added to this project.")
    return success({"members": project.getMemberList()})
