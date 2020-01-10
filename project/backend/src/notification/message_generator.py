def generateNotificationMessage(triggerUser, projectName, type, issueNumber):
    if type == "new_comment":
        return "User {} commented on project {} issue #{}".format(triggerUser, projectName, issueNumber)
    elif type == "new_issue":
        return "User {} added a new issue (#{}) to project {}".format(triggerUser, issueNumber, projectName)
    elif type == "change_attribute":
        return "User {} changed attribute of issue #{} of project {}".format(triggerUser, issueNumber, projectName)
    return "Something unknown triggered a notification, report to dev team to resolve this problem."
