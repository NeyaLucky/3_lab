from flask import jsonify, request, Flask
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Playlist'
mongo = PyMongo(app)
SWAGGER_UPL = '/swagger'
API_UPL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_UPL,
    API_UPL,
    config={
        'Playlist': "Todo list API"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_UPL)


class CollectionResource:
    def __init__(self, collection_name, required_fields=None):
        self.collection_name = collection_name
        self.required_fields = required_fields or []

    def validate_required_fields(self, data):
        missing_fields = [field for field in self.required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        return None

    def get_all(self):
        items = mongo.db[self.collection_name].find()
        return jsonify({f'{self.collection_name.lower()}': items})

    def get_by_id(self, item_id):
        item = mongo.db[self.collection_name].find_one({'_id': item_id})
        return jsonify({f'{self.collection_name.lower()}': item})

    def create(self):
        new_item = request.json

        # Validate required fields
        validation_result = self.validate_required_fields(new_item)
        if validation_result:
            return validation_result

        # Insert the new item into the MongoDB collection
        item_id = mongo.db[self.collection_name].insert(new_item)
        return jsonify({f'{self.collection_name.lower()}_id': str(item_id)})

    def update(self, item_id):
        updated_item_data = request.json
        mongo.db[self.collection_name].update_one({'_id': item_id}, {'$set': updated_item_data})
        return jsonify({'message': f'{self.collection_name} updated successfully'})

    def delete(self, item_id):
        mongo.db[self.collection_name].delete_one({'_id': item_id})
        return jsonify({'message': f'{self.collection_name} deleted successfully'})


class UserResource(CollectionResource):
    def __init__(self):
        super().__init__('User', required_fields=['email', 'name'])


class PlaylistResource(CollectionResource):
    def __init__(self):
        super().__init__('Playlist', required_fields=['name'])


class PlaylistAccessResource(CollectionResource):
    def __init__(self):
        super().__init__('PlaylistAccess', required_fields=['user_id', 'playlist_id'])


class PlaylistSongResource(CollectionResource):
    def __init__(self):
        super().__init__('PlaylistSong', required_fields=['playlist_id', 'song_id'])


class SongResource(CollectionResource):
    def __init__(self):
        super().__init__('Song', required_fields=['title', 'artist'])
@app.route('/user', methods=['GET', 'POST'])
def user():
    """Endpoint to get all users or create a new user."""
    user_resource = UserResource()
    if request.method == 'GET':
        return user_resource.get_all()
    elif request.method == 'POST':
        return user_resource.create()


@app.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(user_id):
    """Endpoint to get, update, or delete a user by ID."""
    user_resource = UserResource()
    if request.method == 'GET':
        return user_resource.get_by_id(user_id)
    elif request.method == 'PUT':
        return user_resource.update(user_id)
    elif request.method == 'DELETE':
        return user_resource.delete(user_id)


@app.route('/playlists', methods=['GET', 'POST'])
def playlists():
    """Endpoint to get all playlists or create a new playlist."""
    playlist_resource = PlaylistResource()
    if request.method == 'GET':
        return playlist_resource.get_all()
    elif request.method == 'POST':
        return playlist_resource.create()


@app.route('/playlists/<playlist_id>', methods=['GET', 'PUT', 'DELETE'])
def playlist(playlist_id):
    """Endpoint to get, update, or delete a playlist by ID."""
    playlist_resource = PlaylistResource()
    if request.method == 'GET':
        return playlist_resource.get_by_id(playlist_id)
    elif request.method == 'PUT':
        return playlist_resource.update(playlist_id)
    elif request.method == 'DELETE':
        return playlist_resource.delete(playlist_id)


@app.route('/playlistaccess', methods=['GET', 'POST'])
def playlistaccess():
    """Endpoint to get all playlist access or create a new playlist access."""
    playlistaccess_resource = PlaylistAccessResource()
    if request.method == 'GET':
        return playlistaccess_resource.get_all()
    elif request.method == 'POST':
        return playlistaccess_resource.create()


@app.route('/playlistaccess/<playlistaccess_id>', methods=['GET', 'PUT', 'DELETE'])
def get_playlist_access(playlistaccess_id):
    """Endpoint to get, update, or delete a playlist access by ID."""
    playlistaccess_resource = PlaylistAccessResource()
    if request.method == 'GET':
        return playlistaccess_resource.get_by_id(playlistaccess_id)
    elif request.method == 'PUT':
        return playlistaccess_resource.update(playlistaccess_id)
    elif request.method == 'DELETE':
        return playlistaccess_resource.delete(playlistaccess_id)


@app.route('/playlistsong', methods=['GET', 'POST'])
def playlistsong():
    """Endpoint to get all playlist songs or create a new playlist song."""
    playlistsong_resource = PlaylistSongResource()
    if request.method == 'GET':
        return playlistsong_resource.get_all()
    elif request.method == 'POST':
        return playlistsong_resource.create()


@app.route('/playlistsong/<playlistsong_id>', methods=['GET', 'PUT', 'DELETE'])
def get_playlist_song(playlistsong_id):
    """Endpoint to get, update, or delete a playlist song by ID."""
    playlistsong_resource = PlaylistSongResource()
    if request.method == 'GET':
        return playlistsong_resource.get_by_id(playlistsong_id)
    elif request.method == 'PUT':
        return playlistsong_resource.update(playlistsong_id)
    elif request.method == 'DELETE':
        return playlistsong_resource.delete(playlistsong_id)


@app.route('/songs', methods=['GET', 'POST'])
def songs():
    """Endpoint to get all songs or create a new song."""
    song_resource = SongResource()
    if request.method == 'GET':
        return song_resource.get_all()
    elif request.method == 'POST':
        return song_resource.create()


@app.route('/songs/<song_id>', methods=['GET', 'PUT', 'DELETE'])
def get_song(song_id):
    """Endpoint to get, update, or delete a song by ID."""
    song_resource = SongResource()
    if request.method == 'GET':
        return song_resource.get_by_id(song_id)
    elif request.method == 'PUT':
        return song_resource.update(song_id)
    elif request.method == 'DELETE':
        return song_resource.delete(song_id)


if __name__ == '__main__':
    app.run(debug=True)
