from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Playlist']

class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration

    def save(self):
        db.songs.insert_one({
            "title": self.title,
            "artist": self.artist,
            "duration": self.duration
        })

    @staticmethod
    def find_by_title(title):
        return db.songs.find_one({"title": title})

