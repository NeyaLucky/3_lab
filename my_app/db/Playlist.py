from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Playlist']

class Playlist:
    def __init__(self, title, is_public, owner_id, songs=None):
        self.title = title
        self.is_public = is_public
        self.owner_id = owner_id
        self.songs = songs or []

    def save(self):
        db.playlists.insert_one({
            "title": self.title,
            "is_public": self.is_public,
            "owner_id": self.owner_id,
            "songs": self.songs
        })

    @staticmethod
    def find_by_title(title):
        return db.playlists.find_one({"title": title})

    @staticmethod
    def find_by_owner(owner_id):
        return db.playlists.find({"owner_id": owner_id})

    @staticmethod
    def find_public_playlists():
        return db.playlists.find({"is_public": True})
