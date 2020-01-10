import unittest
from src.its_model.user import ItsUser
from src.its_model.user_manager import UserManager
class TestUser(unittest.TestCase):
    def setUp(self):
        self.tearDown()
        userManager = UserManager()
        userManager.deleteUser({
        "username": "pythonut"
        })
        userManager.createUser({
        "username": "pythonut",
        "name": "Python Unit Test",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid",
        "role": "user",
        "password": "pythonut"
        })
        userManager.createUser({
        "username": "pythonut2",
        "name": "Python Unit Test2",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid2",
        "role": "user",
        "password": "pythonut2"
        })

    def test_user_not_found(self):
        user = ItsUser("pythonut")
        with self.assertRaises(Exception):
            user.getProfile("notFound")

    def test_get_project_id(self):
        user = ItsUser("pythonut")
        user.createProject("pythonUnitTest")
        self.assertTrue(user.getProjectId("pythonUnitTest") in [project["project_id"] for project in user.getOwnerProjects()])
        with self.assertRaises(Exception):
            user.getProjectId("projectNotExist")
        user.deleteProject("pythonUnitTest")

    def test_get_user_profile(self):
        user = ItsUser("pythonut")
        self.assertEqual(user.getProfile(), {
        "username": "pythonut",
        "name": "Python Unit Test",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid",
        "isOwner": True
        })

        self.assertEqual(user.getProfile("pythonut"), {
        "username": "pythonut",
        "name": "Python Unit Test",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid",
        "isOwner": True
        })

    def test_update_user_profile(self):
        user = ItsUser("pythonut")
        user.updateProfile({"email": "pythonut2@gmail.com",
                                "lineID": "unittestlineid2",
                                "name": "Python Unit Test2"})
        self.assertEqual(user.getProfile(), {
        "username": "pythonut",
        "name": "Python Unit Test2",
        "email": "pythonut2@gmail.com",
        "lineID": "unittestlineid2",
        "isOwner": True
        })
        user.updateProfile({"email": "pythonut@gmail.com",
                                "lineID": "unittestlineid",
                                "name": "Python Unit Test"})
        self.assertEqual(user.getProfile(), {
        "username": "pythonut",
        "name": "Python Unit Test",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid",
        "isOwner": True
        })
    def test_get_other_user_profile(self):
        user = ItsUser("pythonut")
        self.assertEqual(user.getProfile("pythonut2"), {
        "username": "pythonut2",
        "name": "Python Unit Test2",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid2",
        "isOwner": False
        })


    def test_get_project_list(self):
        user = ItsUser("pythonut")
        user.createProject("pythonUnitTest")
        self.assertTrue({
            'username': 'pythonut',
            'project_name': 'pythonUnitTest'} in user.getProjectList())
        user.deleteProject("pythonUnitTest")

    def test_create_project(self):
        user = ItsUser("pythonut")
        user.createProject("pythonUnitTest")
        self.project_should_own_by_user(user, "pythonUnitTest")
        with self.assertRaises(Exception):
            user.createProject("pythonUnitTest")
        user.deleteProject("pythonUnitTest")

    def test_password_checker(self):
        user = ItsUser("pythonut")
        self.assertTrue(user.isPasswordCorrect("pythonut"))
        self.assertFalse(user.isPasswordCorrect("errorPassword"))

    def test_update_password(self):
        user = ItsUser("pythonut")
        user.updatePassword("pythonut", "newpythonut")
        self.assertTrue(user.isPasswordCorrect("newpythonut"))
        with self.assertRaises(Exception):
            user.updatePassword("pythonut", "newpythonut")


    def project_should_own_by_user(self, user, projectName):
        self.assertTrue(projectName in [projectDict["project_name"] for projectDict in user.getOwnerProjects()])


    def tearDown(self):
        userManager = UserManager()
        userManager.deleteUser({
        "email": "pythonut@gmail.com"
        })


if __name__ == '__main__':
    unittest.main()
