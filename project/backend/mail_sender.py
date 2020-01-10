import smtplib
from email.mime.text import MIMEText

# remove sensitive information when commit
gmail_user = "issue.tracking.notify@gmail.com"
gmail_password = ""

# Preset mail for convenience
defaultFooterMsg = (
"""
-- Issue Tracking System Automantic Notification

*You received this mail because you are an assignee of the project mentioned above.*
*If you believed this is a mistake, report to this mail address and mention the problem you've occured.*
"""
)

def generateIssueAddNotify(user, issue, issueNumber, project):
    return (
    """
    Hi,
    User {} has submitted an issue {} #{} to {}

    <Footer>
    """.format(user, issue, issueNumber, project)).replace("<Footer>", defaultFooterMsg)

def generateIssueCommentNotify(user, issue, issueNumber, project):
    return (
    """
    Hi,
    User {} has commented to an issue {} #{} in project {}

    <Footer>
    """.format(user, issue, issueNumber, project)).replace("<Footer>", defaultFooterMsg)

def generateAssignNotify(user, issue, issueNumber, project):
    return (
    """
    Hi,
    You have been assigned to an issue ({} #{}) of project {} by {}

    <Footer>
    """.format(issue, issueNumber, project, user)).replace("<Footer>", defaultFooterMsg)

def readMailPassword():
    global gmail_password
    from security_reader import SecurityReader
    securityReader = SecurityReader()
    gmail_password = securityReader.getMailPasswd()
    securityReader.close()

class MailSender:
    def __init__(self):
        readMailPassword()
        if gmail_password != "":
            self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            self.server.ehlo()
            self.server.login(gmail_user, gmail_password)
            self.message = None
        else:
            print("[ERROR]: Problem occured when reading secret mix")

    def setMailInfo(self, targetAddress,
                    subject="<No Subject>",
                    text="<No Message>"):
        self.message = MIMEText(text)
        self.message["Subject"] = subject
        self.message["To"] = targetAddress
        self.targetAddress = targetAddress

    def sendMail(self):
        if self.server and self.message:
            self.server.sendmail(gmail_user,
                                 self.targetAddress,
                                 self.message.as_string())
            print("[INFO]: Send mail via Google SMTP")
        elif not self.message:
            print("[ERROR]: Set mail info before send")
        elif not self.server:
            print("[ERROR]: Server login failed")

    def close(self):
        self.server.quit()

# testing function
if __name__ == "__main__":
    import sys
    print("[TEST]: Testing mail sending")
    sender = MailSender()
    sender.setMailInfo(sys.argv[1], "test", generateIssueAddNotify(1, 2, 3, 4))
    sender.sendMail()
    sender.close()
    print("[TEST]: Done!")
