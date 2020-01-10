from flask import Blueprint, render_template, send_from_directory, request
from mongo import mongo, getProjectId
from login_required import login_required, project_member_required
from bson import json_util
from line_notifier import LineNotifier
from mail_sender import (MailSender, generateIssueAddNotify, generateIssueCommentNotify, generateAssignNotify)
import json
import datetime
from .its_model.project import Project
from .response import redirect, success, failure



issue_bp = Blueprint('issue', __name__, url_prefix='/issue')
def generateNotification(username, projectId, type, issueNumber):
    result = mongo.db.project.find_one({"_id": projectId})
    if type == "new_comment":
        return "User {} commented on project {} issue #{}".format(username, result["project_name"], issueNumber)
    elif type == "new_issue":
        return "User {} added a new issue (#{}) to project {}".format(username, issueNumber, result["project_name"])
    elif type == "change_attribute":
        return "User {} changed attribute of issue #{} of project {}".format(username, issueNumber, result["project_name"])
    return "Something unknown triggered a notification, report to dev team to resolve this problem."

def getAssigneeProfile(projectId, issueNumber):
    issue = mongo.db.issue.find_one({"project_id": projectId,
                                     "issue_number": issueNumber})
    assignees = issue["assignees"]
    userProfiles = []
    for name in assignees:
        profile = mongo.db.user_profile.find_one({"username": name})
        userProfiles.append(profile)
    return userProfiles

# TODO: refine notification code, this looks so bad :((((
def notifyByLine(projectId, issueNumber, type, triggerUser="**"):
    lineNotifier = LineNotifier()
    assignees = getAssigneeProfile(projectId, issueNumber)
    lineId = []
    for user in assignees:
        lineId.append(user["lineID"])

    if lineId:
        lineNotifier.sendNotification(generateNotification(triggerUser, projectId, type, issueNumber),
                                      lineId)

def notifyByEmail(projectId, issueNumber, type, triggerUser="**"):
    mailSender = MailSender()
    assignees = getAssigneeProfile(projectId, issueNumber)
    mailAddress = []
    for user in assignees:
        mailSender.setMailInfo(user["email"],
                               "Issue Tracking System Notificaion",
                               generateNotification(triggerUser, projectId, type, issueNumber))
        mailSender.sendMail()
    mailSender.close()

@issue_bp.route('/get_issue_content', methods=["POST"])
@login_required
@project_member_required
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
def getIssueListData():
    try:
        project = Project(request.get_json()["username"], request.get_json()["project_name"])
    except:
        return redirect(404)
    return success(project.getIssueList())

@issue_bp.route('/new_comment', methods=["POST"])
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
    # notify via line
    # notifyByLine(projectId=issue["project_id"],
    #              issueNumber=issue["issue_number"],
    #              type="new_comment",
    #              triggerUser=request.cookies.get('id'))
    # notifyByEmail(projectId=issue["project_id"],
    #              issueNumber=issue["issue_number"],
    #              type="new_comment",
    #              triggerUser=request.cookies.get('id'))

    return success(issue.getData())
@issue_bp.route('/new', methods=["POST"])
def addNewIssue():
    requestDict = request.get_json()
    try:
        project = Project(requestDict["username"], requestDict["project_name"])

    except:
        return redirect(404)
    new_issue_number = project.createIssue(request.cookies.get('id'), requestDict)
    # notifyByLine(projectId=project_id,
    #              issueNumber=new_issue_number,
    #              type="new_issue",
    #              triggerUser=request.cookies.get('id'))
    # notifyByEmail(projectId=project_id,
    #              issueNumber=new_issue_number,
    #              type="new_issue",
    #              triggerUser=request.cookies.get('id'))

    return redirect(requestDict["username"] + "/" + requestDict["project_name"] + "/issues/" + str(new_issue_number))

@issue_bp.route('/change_attribute', methods=["POST"])
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

    # notifyByLine(projectId=issue["project_id"],
    #              issueNumber=issue["issue_number"],
    #              type="change_attribute",
    #              triggerUser=request.cookies.get('id'))
    # notifyByEmail(projectId=issue["project_id"],
    #              issueNumber=issue["issue_number"],
    #              type="change_attribute",
    #              triggerUser=request.cookies.get('id'))

    return success(issue.getData())

@issue_bp.route('/change_assignee', methods=["POST"])
@login_required
@project_member_required
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


    # notifyByLine(projectId=issue["project_id"],
    #              issueNumber=issue["issue_number"],
    #              type="change_attribute",
    #              triggerUser=request.cookies.get('id'))
    # notifyByEmail(projectId=issue["project_id"],
    #              issueNumber=issue["issue_number"],
    #              type="change_attribute",
    #              triggerUser=request.cookies.get('id'))

    return success(issue.getData())
