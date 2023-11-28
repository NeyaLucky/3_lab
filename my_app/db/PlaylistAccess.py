from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['Playlist']

class PlaylistAccess:
    def __init__(self, playlist_id, user_id):
        self.playlist_id = playlist_id
        self.user_id = user_id

    def save(self):
        db.playlist_access.insert_one({
            'playlist_id': self.playlist_id,
            'user_id': self.user_id
        })

    @staticmethod
    def find_users_with_access(playlist_id):
        access_list = db.playlist_access.find({'playlist_id': playlist_id})
        return [access['user_id'] for access in access_list]