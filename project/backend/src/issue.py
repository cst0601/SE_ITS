from flask import Blueprint, render_template, send_from_directory, request
from .its_model.mongo import mongo
from .its_model.login_verification import LoginVerification
from bson import json_util
from .notification.line_notifier import lineNotifier
from .notification.mail_sender import mailSender
import json
import datetime
from .its_model.project import Project
from .response import redirect, success, failure

issue_bp = Blueprint('issue', __name__, url_prefix='/issue')
@issue_bp.route('/get_issue_content', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def getIssueContent():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    try:
        issue = project.getIssue(request.get_json()["issue_number"])
    except:
        return failure("Issue not exist.")
    return success(issue.getData())

@issue_bp.route('/list', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def getIssueListData():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    return success(project.getIssueList())

@issue_bp.route('/new_comment', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def addNewComment():
    requestDict = request.get_json()
    try:
        project = Project(requestDict["username"], requestDict["project_name"])
    except:
        return redirect(404)
    try:
        issue = project.getIssue(requestDict["issue_number"])
    except:
        return failure("Issue not exist.")
    issue.addNewComment(request.cookies.get('id'), requestDict["comment"])

    lineNotifier.sendNotification(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )
    mailSender.sendEmail(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )
    return success(issue.getData())
@issue_bp.route('/new', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def addNewIssue():
    requestDict = request.get_json()
    try:
        project = Project(requestDict["username"], requestDict["project_name"])

    except:
        return redirect(404)
    new_issue_number = project.createIssue(request.cookies.get('id'), requestDict)
    issue = project.getIssue(new_issue_number)
    lineNotifier.sendNotification(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )
    mailSender.sendEmail(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )
    return redirect(requestDict["username"] + "/" + requestDict["project_name"] + "/issues/" + str(new_issue_number))

@issue_bp.route('/change_attribute', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def changeAttribute():
    requestDict = request.get_json()
    try:
        project = Project(requestDict["username"], requestDict["project_name"])
    except:
        return redirect(404)
    try:
        issue = project.getIssue(requestDict["issue_number"])
    except:
        return failure("Issue not exist.")
    try:
        issue.changeAttribute(request.cookies.get('id'), requestDict["change_detail"])
    except:
        return failure("Key error.")

    lineNotifier.sendNotification(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )
    mailSender.sendEmail(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )

    return success(issue.getData())

@issue_bp.route('/change_assignee', methods=["POST"])
@LoginVerification.login_required
@LoginVerification.project_member_required
def changeAssignee():
    requestDict = request.get_json()
    try:
        project = Project(requestDict["username"], requestDict["project_name"])
    except:
        return redirect(404)
    try:
        issue = project.getIssue(requestDict["issue_number"])
    except:
        return failure("Issue not exist.")
    try:
        issue.changeAssignee(request.cookies.get('id'), requestDict["change_detail"])
    except:
        return failure("Action error.")

    lineNotifier.sendNotification(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )
    mailSender.sendEmail(
        project=project,
        issue=issue,
        type="change_attribute",
        triggerUser=request.cookies.get('id')
    )
    return success(issue.getData())
