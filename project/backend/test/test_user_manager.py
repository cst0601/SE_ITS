import unittest
from src.its_model.user_manager import UserManager
from src.its_model.user import ItsUser
class TestUserManager(unittest.TestCase):
    def setUp(self):
        userManager = UserManager()
        userManager.createUser({
        "username": "pythonut",
        "name": "Python Unit Test",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid",
        "role": "user",
        "password": "pythonut"
        })

    def test_create_user(self):
        userManager = UserManager()
        userManager.createUser({
        "username": "pythonut3",
        "name": "Python Unit Test2",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid2",
        "role": "user",
        "password": "pythonut2"
        })
        usernames = [user["username"] for user in userManager.getUsers()]
        self.assertTrue("pythonut3" in usernames)

    def test_get_users(self):
        userManager = UserManager()
        userManager.deleteUser({
        "username": "pythonut2"
        })
        usernames = [user["username"] for user in userManager.getUsers()]
        self.assertTrue("pythonut" in usernames)
        self.assertFalse("pythonut2" in usernames)

        userManager.createUser({
        "username": "pythonut2",
        "name": "Python Unit Test2",
        "email": "pythonut@gmail.com",
        "lineID": "unittestlineid2",
        "role": "user",
        "password": "pythonut2"
        })
        usernames = [user["username"] for user in userManager.getUsers()]
        self.assertTrue("pythonut" in usernames)
        self.assertTrue("pythonut2" in usernames)


    def test_create_duplicated_user(self):
        userManager = UserManager()
        with self.assertRaises(Exception):
            userManager.createUser({
            "username": "pythonut",
            "name": "Python Unit Test2",
            "email": "pythonut@gmail.com",
            "lineID": "unittestlineid2",
            "role": "user",
            "password": "pythonut2"
            })
    def test_update_role(self):
        userManager = UserManager()
        userManager.updateRole("pythonut", "manager")
        role = [user["role"] for user in userManager.getUsers() if user["username"] == "pythonut"][0]
        self.assertEqual(role, "manager")
        with self.assertRaises(Exception):
            userManager.updateRole("notExist", "manager")

    def tearDown(self):
        userManager = UserManager()
        userManager.deleteUser({
        "email": "pythonut@gmail.com"
        })


if __name__ == '__main__':
    unittest.main()
