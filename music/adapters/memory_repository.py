import csv, ast, random
from pathlib import Path

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel import album, artist, genre, playlist, review, track, user


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__tracks = []
        self.__albums = []
        self.__artists = []
        self.__genres = []
        self.__users = []
        self.__reviews = []
        # self.__playlists = {} #TODO ?
        self.__track_dict = {}
        self.__sorted_tracks = []
        self.__high_reviewed_tracks = []
        self.__recommended_tracks = []

    #def create_user(self, username, password):

    def add_user(self, new_user: user):
        super().add_user(new_user)
        self.__users.append(new_user)

    """def remove_user(self, user_name: str):
        # TODO - Current ID method will not work when this is implemented, need to rethink it
        pass"""

    def get_user(self, user_name: str):
        for user_object in self.__users:
            if user_object.user_name.lower() == user_name.lower():
                return user_object
        return None

    def add_review_to_user(self, current_user: user.User, new_review: review.Review):
        flag = True
        for old_review in range(len(current_user.reviews)): # check if review is in user obj
            if current_user.reviews[old_review].track.track_id == new_review.track.track_id:
                flag = False
                current_user.reviews[old_review] = new_review # replace if review is in user obj
                return None
        if flag:
            current_user.add_review(new_review)

    def add_review_to_track(self, current_track: track.Track, new_review: review.Review, current_user: user.User):
        flag = True
        for old_track in range(len(current_track.reviews)): # check if review is in track obj
            if current_track.reviews[old_track].review_user == current_user:
                flag = False
                current_track.reviews[old_track] = new_review # replace if review is in track obj
                return None
        if flag:
            current_track.add_review(new_review)

    """def get_user_count(self) -> int:
        return len(self.__users)"""

    """def get_user_reviews(self, user_name: str) -> list[review]:
        for user_object in self.__users:
            if user_object.user_name == user_name:
                return user_object.reviews
        return []"""

    """def get_all_reviews(self) -> list[review]:
        return self.__reviews"""

    """def get_reviews_by_track(self, track_object: track) -> list[review]:
        return_list = []
        for review_object in self.__reviews:
            if review_object.track == track_object:
                return_list.append(review_object)
        return return_list"""

    """def add_user_review(self, user_object: user, track_object: track, review_text:str, rating: int) -> bool:
        try:
            new_review = review.Review(track_object, review_text, rating, user_object)
            user_object.add_review(new_review)
            self.__reviews.append(new_review)
            return True
        except:
            return False"""

    """def remove_user_review(self, user_object: user, review_object: review):
        if review_object in self.__reviews:
            self.__reviews.remove(review_object)
            user_object.user.remove_review(review_object)"""

    """def get_user_liked_tracks(self, user_name: str) -> list[track]:
        for user_object in self.__users:
            if user_object.user.user_name == user_name:
                return user_object.liked_tracks
        return []"""

    """def add_user_liked_track(self, user_name: str, track_object: track):
        for user_object in self.__users:
            if user_object.user.user_name == user_name:
                user_object.user.add_liked_track(track_object)"""

    """def get_user_playlists(self, user_name: str) -> list[playlist]:
        for user_object in self.__users:
            if user_object.user.user_name == user_name:
                return user_object.user.playlists

    def get_user_playlist(self, user_name: str, playlist_object: playlist) -> list[track]:
        for user_object in self.__users:
            if user_object.user.user_name == user_name and playlist_object in user_object.user.playlists:
                return playlist_object.tracks

    def get_all_playlists(self) -> list[playlist]:
        # TODO ?
         Returns all playlists across users --> Integrate following dict method if we want this
        playlist = {}
        def add(user, new_playlist):
            if user in playlist:
                if new_playlist not in playlist[user]:
                    playlist[user].append(new_playlist)
            else:
                playlist[user] = [new_playlist]
        
        raise NotImplementedError

    def add_playlist(self, user_name: str, playlist_object: playlist):
        for user_object in self.__users:
            if user_object.user.user_name == user_name:
                user_object.user.add_playlist(playlist_object)

    def remove_playlist(self, user_name: str, playlist_object: playlist):
        for user_object in self.__users:
            if user_object.user.user_name == user_name:
                user_object.user.remove_playlist(playlist_object)

    def add_to_playlist(self, playlist_object: playlist, track_object: track):
        playlist_object.playlist.add_track(track)

    def remove_from_playlist(self, playlist_object: playlist, track_object: track):
        playlist_object.playlist.remove_track(track)

    def get_playlist_duration(self, playlist_object: playlist):
        duration = 0
        for track_object in playlist_object.playlist.tracks():
            duration += track_object.track.track_duration
        return duration

    def get_playlist_size(self, playlist_object: playlist):
        return playlist_object.playlist.size()"""

    def add_track(self, new_track: track):
        super().add_track(new_track)
        self.__tracks.append(new_track)

    def add_track_to_sort(self, new_track: track):
        super().add_track(new_track)
        self.__sorted_tracks.append(new_track)

    def get_sorted_tracks(self):
        return self.__sorted_tracks

    def get_track(self, track_id: int) -> track:
        for track_object in self.__tracks:
            if track_object.track_id == track_id:
                return track_object
        return None

    """def get_tracks_by_duration(self, duration: int) -> list[track]:
        return_tracks = []
        for track_object in self.__tracks:
            if track_object.track_duration - 10 <= duration <= track_object.track_duration + 10:
                return_tracks.append(track_object)
        return return_tracks"""

    """def get_track_url(self, track_id: int):
        for track_object in self.__tracks:
            if track_object.track_id == track_id:
                return track_object.track_url
        return None"""

    """def get_track_genres(self, track_id: int) -> list[genre]:
        for track_object in self.__tracks:
            if track_object.track_id == track_id:
                return track_object.genres
        return []"""

    def get_number_of_tracks(self) -> int:
        return len(self.__tracks)

    """def get_first_track(self) -> track:
        # TODO: Decide whether we want to sort the tracks specifically or just by when added
        return self.__tracks[0]

    def get_last_track(self) -> track:
        # TODO: Decide whether we want to sort the tracks specifically or just by when added
        return self.__tracks[-1]

    def get_first_thirty_tracks(self) -> list:
        return self.__tracks[0:49]"""

    def get_list_of_tracks(self, page_start: int, songs_per_page: int) -> list[track.Track]:
        first_track = (page_start-1)*songs_per_page
        last_track = first_track+songs_per_page
        return self.__sorted_tracks[first_track:last_track]

    """def get_tracks_by_album(self, album_id: int) -> list[track]:
        return_tracks = []
        for track_object in self.__tracks:
            if track_object.album.album_id == album_id:
                return_tracks.append(track_object)
        return return_tracks"""

    """def get_track_album(self, track_obj: track) -> album:
        for track_object in self.__tracks:
            if track_object == track_obj:
                return track_object.album
        return None"""

    """def get_tracks_by_artist(self, artist_id: int) -> list[track]:
        return_tracks = []
        for track_object in self.__tracks:
            if track_object.artist.artist_id == artist_id:
                return_tracks.append(track_object)
        return return_tracks

    def get_track_artist(self, track_obj: track) -> artist:
        for track_object in self.__tracks:
            if track_object == track_obj:
                return track_object.artist
        return None"""

    def add_album(self, new_album: album):
        super().add_album(new_album)
        self.__albums.append(new_album)

    def get_albums(self) -> list[album.Album]:
        return self.__albums
    
    def get_album(self, index: int) -> album.Album:
        for check_album in self.__albums:
            if check_album.album_id == index:
                return check_album

    def add_artist(self, new_artist: artist):
        super().add_artist(new_artist)
        self.__artists.append(new_artist)

    def get_artists(self) -> list[artist.Artist]:
        return self.__artists
    
    def get_artist(self, index: int) -> artist.Artist:
        for check_artist in self.__artists:
            if check_artist.artist_id == index:
                return check_artist

    def add_genre(self, new_genre: genre):
        super().add_genre(new_genre)
        self.__genres.append(new_genre)

    def get_genres(self) -> list[genre.Genre]:
        return self.__genres

    def add_track_dict(self, track_object: track, track_album: album, track_artist: artist):
        self.__track_dict[track_object] = [track_object.title, track_album.title, track_artist.full_name]

    def get_track_dict(self):
        return self.__track_dict

    def return_track_from_dict(self, input):
        input = input.lower()
        return_list = []
        for track_obj in self.__track_dict:
            for item in self.__track_dict[track_obj]:
                if input in item.lower():
                    return_list.append(track_obj)
                    if len(return_list) == 30:
                        return return_list
        return return_list

    def sort_tracks(self, function: str, order: bool):
        """
        input -> Function name to find method to sort by
                (All functions below)
        order -> True = Descending, False = Ascending
        EXAMPLES: album name asc = sort_tracks(get_track_album_name, False)
                  track name desc = sort_tracks(get_track_name, True)
        """

        function = "self." + function

        self.__sorted_tracks = sorted(self.__tracks, reverse=order, key=eval(function))

    def get_track_name(self, track_obj):
        return track_obj.title

    def get_track_id(self, track_obj):
        return track_obj.track_id

    def get_track_duration(self, track_obj):
        return track_obj.track_duration

    def get_track_artist_name(self, track_obj):
        return track_obj.artist.full_name

    def get_track_album_name(self, track_obj):
        return track_obj.album.title

    def get_track_rating(self, track_obj):
        return track_obj.average_rating()

    def recommend_tracks(self, user_object: user):
        self.__high_reviewed_tracks.clear()
        self.__recommended_tracks.clear()
        for user_review in user_object.reviews:
            if user_review.rating > 3:
                self.__high_reviewed_tracks.append(user_review.track)
        for high_reviewed_track in self.__high_reviewed_tracks:
            for track_object in self.__tracks:
                self.recommend_from_artist(high_reviewed_track, track_object)
                self.recommend_from_genre(high_reviewed_track, track_object)
                self.recommend_from_album(high_reviewed_track, track_object)
                self.recommend_from_duration(high_reviewed_track, track_object)
        random.shuffle(self.__recommended_tracks)
        if len(self.__recommended_tracks) > 10:
            self.__recommended_tracks = self.__recommended_tracks[0:10]
        return self.__recommended_tracks

    def recommend_from_artist(self, high_reviewed_track, track_object):
        if high_reviewed_track.artist == track_object.artist and high_reviewed_track != track_object and track_object not in self.__recommended_tracks:
            self.__recommended_tracks.append(track_object)

    def recommend_from_genre(self, high_reviewed_track, track_object):
        for genre_type in high_reviewed_track.genres:
            if genre_type in track_object.genres and high_reviewed_track != track_object and track_object not in self.__recommended_tracks:
                self.__recommended_tracks.append(track_object)

    def recommend_from_album(self, high_reviewed_track, track_object):
        if high_reviewed_track.album == track_object.album and high_reviewed_track != track_object and track_object not in self.__recommended_tracks:
            self.__recommended_tracks.append(track_object)

    def recommend_from_duration(self, high_reviewed_track, track_object):
        if high_reviewed_track.track_duration-15 <= track_object.track_duration <= high_reviewed_track.track_duration+15 and high_reviewed_track != track_object and track_object not in self.__recommended_tracks:
            self.__recommended_tracks.append(track_object)

    def generate_user_id(self):
        return len(self.__users) + 1

    def get_users(self):
        return self.__users

    def read_csv_file(filename: str):
        with open(filename, encoding="unicode_escape") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                row = [item.strip() for item in row]
                yield row


def load_tracks(data_path: Path, repo: MemoryRepository):
    tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    for row in MemoryRepository.read_csv_file(tracks_filename):
        if row[0] == "track_id":
            continue
        track_name_fixed = row[37].replace('&amp;', '&')
        new_track = track.Track(int(row[0]), track_name_fixed)
        if row[1] == "":
            new_track.album = album.Album(0, "None")
        else:
            album_name_fixed = row[2].replace('&amp;', '&')
            new_track.album = album.Album(int(row[1]), album_name_fixed)
        if row[4] == "":
            new_track.artist = artist.Artist(0, "None")
        else:
            artist_name_fixed = row[5].replace('&amp;', '&')
            new_track.artist = artist.Artist(int(row[4]), artist_name_fixed)
        if row[27] != "":
            for genre_object in ast.literal_eval(row[27]):
                new_genre = genre.Genre(int(genre_object["genre_id"]), genre_object["genre_title"])
                new_track.add_genre(new_genre)
        if row[38] != "":
            new_track.track_url = row[38]
        new_track.track_duration = int(float(row[22]))
        repo.add_track(new_track)
        repo.add_track_to_sort(new_track)
        repo.add_track_dict(new_track, new_track.album, new_track.artist)


def load_albums(data_path: Path, repo: MemoryRepository):
    albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
    for row in MemoryRepository.read_csv_file(albums_filename):
        if row[0] == "album_id":
            continue
        album_name_fixed = row[12].replace('&amp;', '&')
        new_album = album.Album(int(row[0]), album_name_fixed)
        new_album.album_url = row[15]
        new_album.album_type = row[14]
        if row[3] == "":
            new_album.release_year = None
        else:
            new_album.release_year = int(row[3])
        album_list = repo.get_albums()
        if new_album not in album_list:
            repo.add_album(new_album)


def load_artists(data_path: Path, repo: MemoryRepository):
    artists_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    artist_id_list = []
    for row in MemoryRepository.read_csv_file(artists_filename):
        if row[0] == "track_id":
            continue
        if row[4] in artist_id_list:
            continue
        else:
            artist_id_list.append(row[4])
        artist_name_fixed = row[5].replace('&amp;', '&')
        new_artist = artist.Artist(int(row[4]), artist_name_fixed)
        artist_list = repo.get_artists()
        if new_artist not in artist_list:
            repo.add_artist(new_artist)


def load_genres(data_path: Path, repo: MemoryRepository):
    genres_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    for row in MemoryRepository.read_csv_file(genres_filename):
        if row[0] == "track_id":
            continue
        if row[27] != "":
            genre_list = ast.literal_eval(row[27])
        else:
            continue
        track_name_fixed = row[37].replace('&amp;', '&')
        new_track = track.Track(int(row[0]), track_name_fixed)
        for g in genre_list:
            new_genre = genre.Genre(int(g["genre_id"]), g["genre_title"])
            genre_list = repo.get_genres()
            if new_genre not in genre_list:
                new_genre.apply_to(new_track)
                repo.add_genre(new_genre)
            else:
                genres = repo.get_genres()
                for check_genre in genres:
                    if check_genre.genre_id == new_genre.genre_id:
                        check_genre.apply_to(new_track)



def populate(data_path: Path, repo: MemoryRepository):
    load_tracks(data_path, repo)
    load_albums(data_path, repo)
    load_artists(data_path, repo)
    load_genres(data_path, repo)

