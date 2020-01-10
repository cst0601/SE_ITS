"""
line_notifier.py
Notify assignee of an issue via LINE API
"""
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .security_reader import SecurityReader
from ..its_model.user import ItsUser
from .message_generator import generateNotificationMessage
import threading
class LineNotifier:
    def __init__(self):
        securityReader = SecurityReader()
        self.lineApi = LineBotApi(securityReader.getToken())
        securityReader.close()

    def send(self, message, userIdList=[]):
        print(message)
        self.lineApi.multicast(
            userIdList,
            TextSendMessage(text=message)
        )
    def sendNotification(self, project, issue, type, triggerUser):
        message = generateNotificationMessage(
            projectName=project.projectName,
            issueNumber=issue.issueNumber,
            type=type,
            triggerUser=triggerUser)
        assignees = issue.getData()["assignees"]
        assigneeLineIDs = [ItsUser(assignee).getProfile()["lineID"] for assignee in assignees]
        assigneeLineIDs = [assigneeLineID for assigneeLineID in assigneeLineIDs if assigneeLineID != ""]
        if len(assigneeLineIDs) > 0:
            thread = threading.Thread(target = self.send, args = (message, assigneeLineIDs))
            thread.start()
lineNotifier = LineNotifier()
