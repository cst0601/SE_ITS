import unittest
from src.its_model.user import ItsUser
from src.its_model.user_manager import UserManager
from src.its_model.project import Project
class TestProject(unittest.TestCase):
    def setUp(self):
        self.userManager = UserManager()
        self.userManager.deleteUser({
        "email": "pythonut@gmail.com"
        })
        self.userManager.createUser({
        "username": "pythonut",
        "name": "Python Unit Test",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid",
        "role": "user",
        "password": "pythonut"
        })
        self.userManager.createUser({
        "username": "pythonut2",
        "name": "Python Unit Test2",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid2",
        "role": "user",
        "password": "pythonut2"
        })

        self.user = ItsUser("pythonut")
        self.user2 = ItsUser("pythonut2")
        self.create_test_project()

    def create_test_project(self):
        try:
            self.user.deleteProject("ut_project")
            self.user2.deleteProject("ut_project2")
        except:
            pass
        self.user.createProject("ut_project")
        self.user2.createProject("ut_project2")
        self.project = Project("pythonut", "ut_project")
        self.project.addNewMember({
                "username": "pythonut2",
                "manager": True,
                "tester": False,
                "developer": False})
        self.project2 = Project("pythonut2", "ut_project2")

    def test_add_new_comment(self):
        issueNumber = self.create_test_issue(self.project, "pythonut", "Unit test")
        issue = self.project.getIssue(issueNumber)
        issue.addNewComment("pythonut", "UT Comment")
        self.assertTrue("UT Comment" in [comment["comment"] for comment in issue.getData()["comment_list"]])

    def test_change_attribute(self):
        issueNumber = self.create_test_issue(self.project, "pythonut", "Unit test")
        issue = self.project.getIssue(issueNumber)
        issue.changeAttribute("pythonut", {"severity": "high"})
        self.assertEqual("high", issue.getData()["severity"])
        with self.assertRaises(Exception):
            issue.changeAttribute("pythonut", {"notExist": "noUse"})

    def test_change_assignee(self):
        issueNumber = self.create_test_issue(self.project, "pythonut", "Unit test")
        issue = self.project.getIssue(issueNumber)
        issue.changeAssignee("pythonut", {
            "action": "add",
            "assignees": ["pythonut", "pythonut2"],
            "target": "pythonut2"})
        self.assertEqual(["pythonut", "pythonut2"], issue.getData()["assignees"])
        with self.assertRaises(Exception):
            issue.changeAssignee("pythonut", {
                "action": "error",
                "assignees": ["pythonut", "pythonut2"],
                "target": "pythonut2"})

    def tearDown(self):
        try:
            self.user.deleteProject("ut_project")
            self.user2.deleteProject("ut_project2")
        except:
            pass
        self.userManager.deleteUser({
        "email": "pythonut@gmail.com"
        })

    def create_test_issue(self, project, creator,  issueTitle):
        return project.createIssue(creator, {
            "title": issueTitle,
            "severity": "low",
            "priority": "low",
            "reproducible": "no",
            "assignees": [creator],
            "comment": "Test Comment",
        })

if __name__ == '__main__':
    unittest.main()
