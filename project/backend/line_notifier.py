"""
line_notifier.py
Notify assignee of an issue via LINE API
"""
from linebot import LineBotApi
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

class LineNotifier:
    def __init__(self):
        from security_reader import SecurityReader
        securityReader = SecurityReader()
        self.lineApi = LineBotApi(securityReader.getToken())
        securityReader.close()

    def sendNotification(self, message, userIdList=[]):
        self.lineApi.multicast(
            userIdList,
            TextSendMessage(text=message)
        )

# Testing method
if __name__ == "__main__":
    import sys
    print("[TEST] Line notifier")
    ln = LineNotifier()
    ln.sendNotification("some testing message", [sys.argv[1]])
