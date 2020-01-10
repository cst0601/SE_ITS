from flask import Blueprint, send_from_directory, request
from login_required import login_required, its_manager_required
from .its_model.user import ItsUser
from .its_model.user_manager import UserManager
from .response import redirect, success, failure
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profile', methods=["POST"])
@login_required
def getUserProfile():
    user = ItsUser(request.cookies.get('id'))
    profile = user.getProfile(request.get_json()["username"])
    return success(profile)

@user_bp.route('/update_profile', methods=["POST"])
@login_required
def updateUserProfile():
    if request.cookies.get("id") != request.get_json()["username"]:
        return failure("Not acount owner")
    user = ItsUser(request.cookies.get('id'))
    user.updateProfile(request.get_json())
    profile = user.getProfile(request.get_json()["username"])
    return success(profile)

@user_bp.route('/update_password', methods=["POST"])
@login_required
def updateUserPassword():
    if request.cookies.get("id") != request.get_json()["username"]:
        return failure("Not acount owner")
    user = ItsUser(request.cookies.get('id'))
    try:
        user.updatePassword(request.get_json()["oldPassword"], request.get_json()["newPassword"])
    except:
        return failure("Password error")
    return success("Update password succeed")

@user_bp.route('/check', methods=["POST"])
@login_required
def check():
    return success(request.cookies.get('id'))

@user_bp.route('/list', methods=["POST"])
@login_required
@its_manager_required
def getUserList():
    userManager = UserManager()
    return {"info": "success",
            "payload": userManager.getUsers()}

@user_bp.route('/update_role', methods=["POST"])
@login_required
@its_manager_required
def updateRole():
    userManager = UserManager()
    try:
        userManager.updateRole(request.get_json()["selected_username"], request.get_json()["role"])
    except:
        return failure("User not exist.")
    return success(userManager.getUsers())

@user_bp.route('/create_account', methods=["POST"])
@login_required
@its_manager_required
def createAccount():
    userManager = UserManager()
    payload = request.get_json()
    try:
        userManager.createUser(payload)
    except:
        return failure("Username exists")
    userManager.updateRole(payload["username"], payload["role"])
    return success(userManager.getUsers())
