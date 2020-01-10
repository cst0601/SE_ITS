import smtplib
from email.mime.text import MIMEText
from .message_generator import generateNotificationMessage
from .security_reader import SecurityReader
from ..its_model.user import ItsUser
import threading
# remove sensitive information when commit
GMAIL_USER = "issue.tracking.notify@gmail.com"
gmail_password = ""

# Preset mail for convenience
defaultFooterMsg = (
"""
-- Issue Tracking System Automantic Notification

*You received this mail because you are an assignee of the project mentioned above.*
*If you believed this is a mistake, report to this mail address and mention the problem you've occured.*
"""
)

def readMailPassword():
    global gmail_password
    securityReader = SecurityReader()
    gmail_password = securityReader.getMailPasswd()
    securityReader.close()

class MailSender:
    def __init__(self):
        readMailPassword()
        if gmail_password != "":
            self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            self.server.ehlo()
            self.server.login(GMAIL_USER, gmail_password)
        else:
            print("[ERROR]: Problem occured when reading secret mix")

    def sendEmail(self, project, issue, type, triggerUser):
        notificationMessage = generateNotificationMessage(
            projectName=project.projectName,
            issueNumber=issue.issueNumber,
            type=type,
            triggerUser=triggerUser)
        assignees = issue.getData()["assignees"]
        assigneeEmails = [ItsUser(assignee).getProfile()["email"] for assignee in assignees]
        for assigneeEmail in assigneeEmails:
            message = MIMEText(notificationMessage)
            message["Subject"] = "Issue Tracking System Notificaion"
            message["To"] = assigneeEmail
            thread = threading.Thread(target = self.send, args = (assigneeEmail, message))
            thread.start()

    def send(self, targetAddress, message):
        if self.server:
            self.server.sendmail(GMAIL_USER,
                                 targetAddress,
                                 message.as_string())
            print("[INFO]: Send mail via Google SMTP")
        else:
            print("[ERROR]: Server login failed")

    def __del__(self):
        self.server.quit()

mailSender = MailSender()
