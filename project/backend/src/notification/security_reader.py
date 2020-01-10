"""
security_reader.py
Reads application access token and webhook secret.

Created by Chikuma, 2019/12/16

**NOTE** THIS IS THE MODIFIED VERSION OF SecurityReader FROM
LINE_BROADCASTER
"""

class SecurityReader:
    def __init__(self, path="secret_mix/", tokenOnly=False):
        print("[SECURITY] reading secret mix--")
        self.tokenFile = open(path + "token", "r")
        self.passwdFile = open(path + "mail_passwd", "r")

    def getToken(self):
        if self.tokenFile.mode == "r":
            token = self.tokenFile.read()
            token = token.replace("\n", "")
            return token
        return ""

    def getMailPasswd(self):
        if self.passwdFile.mode == "r":
            passwd = self.passwdFile.read()
            passwd = passwd.replace("\n", "")
            return passwd
        return ""

    # Plz remember to close this after reading
    def close(self):
        self.tokenFile.close()
        self.passwdFile.close()
