from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Playlist']

class User:
    def __init__(self, email, username):
        self.email = email
        self.username = username

    def save(self):
        db.users.insert_one({
            "email": self.email,
            "username": self.username
        })

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({"email": email})