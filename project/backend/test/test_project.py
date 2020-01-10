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
        try:
            self.user.deleteProject("ut_project")
            self.user2.deleteProject("ut_project2")
        except:
            pass
        self.user.createProject("ut_project")
        self.user2.createProject("ut_project2")

    def test_get_project(self):
        with self.assertRaises(Exception):
            project = Project("pythonut", "notExist")
        with self.assertRaises(Exception):
            project = Project("notExist", "ut_project")
        with self.assertRaises(Exception):
            project = Project("pythonut2", "ut_project")

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

    def tearDown(self):
        self.user.deleteProject("ut_project")
        self.user2.deleteProject("ut_project2")
        self.userManager.deleteUser({
        "email": "pythonut@gmail.com"
        })

if __name__ == '__main__':
    unittest.main()
