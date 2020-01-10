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

    def test_get_and_update_project_data(self):
        project = Project("pythonut", "ut_project")
        self.assertEqual(project.getData(), {
            "project_name": "ut_project",
            "description": ""
        })
        project.updateDescription("Test, test.")
        self.assertEqual(project.getData(), {
            "project_name": "ut_project",
            "description": "Test, test."
        })

    def test_add_new_member(self):
        project = Project("pythonut", "ut_project")
        self.user_should_not_in_project("pythonut2", project)
        project.addNewMember({
            "username":"pythonut2",
            "manager": False,
            "tester": True,
            "developer": True})
        self.assertTrue({
            'username': 'pythonut2',
            'owner': False,
            'manager': False,
            'tester': True,
            'developer': True,
            'name': 'Python Unit Test2',
            'email': 'pythonut@gmail.com'} in project.getMemberList())
        with self.assertRaises(Exception):
            project.addNewMember({
                "username":"pythonutNotExist",
                "manager": False,
                "tester": True,
                "developer": True})
        with self.assertRaises(Exception):
            project.addNewMember({
                "username":"pythonut2",
                "manager": False,
                "tester": True,
                "developer": True})

    def test_get_member_list(self):
        project = Project("pythonut2", "ut_project2")
        self.assertEqual(project.getMemberList(), [{
            'username': 'pythonut2',
            'owner': True,
            'manager': True,
            'tester': False,
            'developer': False,
            'name': 'Python Unit Test2',
            'email': 'pythonut@gmail.com'}])
        project.addNewMember({
            "username":"pythonut",
            "manager": False,
            "tester": True,
            "developer": True})
        self.assertEqual(project.getMemberList(), [{
            'username': 'pythonut2',
            'owner': True,
            'manager': True,
            'tester': False,
            'developer': False,
            'name': 'Python Unit Test2',
            'email': 'pythonut@gmail.com'}, {
            'username': 'pythonut',
            'manager': False,
            'tester': True,
            'developer': True,
            'owner': False,
            'name': 'Python Unit Test',
            'email': 'pythonut@gmail.com'}])

    def test_get_project_not_exist(self):
        with self.assertRaises(Exception):
            project = Project("pythonut", "notExist")
        with self.assertRaises(Exception):
            project = Project("notExist", "ut_project")
        with self.assertRaises(Exception):
            project = Project("pythonut2", "ut_project")

    def test_update_member_role(self):
        project = Project("pythonut", "ut_project")
        project.addNewMember({
            "username":"pythonut2",
            "manager": False,
            "tester": True,
            "developer": True})
        project.updateMemberRole("pythonut2", {
            "role": "manager",
            "value": True})
        self.assertTrue({
            'username': 'pythonut2',
            'owner': False,
            'manager': True,
            'tester': True,
            'developer': True,
            'name': 'Python Unit Test2',
            'email': 'pythonut@gmail.com'} in project.getMemberList())

        with self.assertRaises(Exception):
            project.updateMemberRole("pythonutNotExist", {
                "role": "manager",
                "value": True})

    def test_is_manager(self):
        project = Project("pythonut", "ut_project")
        project.addNewMember({
            "username":"pythonut2",
            "manager": False,
            "tester": True,
            "developer": True})
        self.assertTrue(project.isManager("pythonut"))
        self.assertFalse(project.isManager("pythonut2"))

    def test_get_issue(self):
        project = Project("pythonut", "ut_project")
        issueNumber = self.create_test_issue(project, "pythonut", "Unit test")
        self.assertTrue(project.getIssue(issueNumber).getData()["title"], "Unit test")
        with self.assertRaises(Exception):
            project.getIssue(-1)
        project.deleteIssue()


    def test_create_issue(self):
        project = Project("pythonut", "ut_project")
        self.create_test_issue(project, "pythonut", "Unit test")
        self.assertTrue("Unit test" in [issue["title"] for issue in project.getIssueList()])
        project.deleteIssue()

    def test_remove_member(self):
        project = Project("pythonut", "ut_project")
        project.addNewMember({
            "username":"pythonut2",
            "manager": False,
            "tester": True,
            "developer": True})
        with self.assertRaises(Exception):
            project.removeMember("not_exist")
        project.removeMember("pythonut2")
        self.user_should_not_in_project("pythonut2", project)

    def test_get_last_issue_id(self):
        project = Project("pythonut", "ut_project")
        self.assertEqual(project.getLastIssueId(), 0)
        self.create_test_issue(project, "pythonut", "Unit test")
        self.assertEqual(project.getLastIssueId(), 1)
        project.deleteIssue()


    def create_test_project(self):
        try:
            self.user.deleteProject("ut_project")
            self.user2.deleteProject("ut_project2")
        except:
            pass
        self.user.createProject("ut_project")
        self.user2.createProject("ut_project2")

    def tearDown(self):
        try:
            self.user.deleteProject("ut_project")
            self.user2.deleteProject("ut_project2")
        except:
            pass
        self.userManager.deleteUser({
        "email": "pythonut@gmail.com"
        })

    def user_should_not_in_project(self, username, project):
        self.assertFalse(username in [member["username"] for member in project.getMemberList()])

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
