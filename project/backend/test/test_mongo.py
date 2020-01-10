import unittest
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from src.its_model.mongo import MONGO_URI, createRoot
client = MongoClient(MONGO_URI)
its = client[parse_uri(MONGO_URI)['database']]
class TestMongo(unittest.TestCase):

    def test_create_root(self):
        its.user_profile.delete_many({"username":"root"})
        createRoot()
        self.assertEqual({
            'username': 'root',
            'name': 'Root',
            'password': 'root',
            'email': 'root@email',
            'lineID': 'root',
            'role': 'manager'}, its.user_profile.find_one({"username": "root"}, {"_id": 0}))
        self.assertEqual("Root account existed.", createRoot())

if __name__ == '__main__':
    unittest.main()
