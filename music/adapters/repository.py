import abc
from typing import List

from music.domainmodel import album, artist, genre, playlist, review, track, user

# Static repo to simulate database
track_repo = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, new_user: user):
        """ Creates a User object and adds it to the repository"""
        if type(new_user) is not user.User:
            raise RepositoryException("User ID should be a non negative integer.")

    '''def remove_user(self, user_name: str):
        """ Removes a User object from the repository"""
        raise NotImplementedError'''

    @abc.abstractmethod
    def get_user(self, user_name: str) -> user:
        """ Returns the User named user_name from the repository
            If no User found, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review_to_user(self, current_user: user.User, new_review: review.Review):
        """ Adds the Review object to the User object if the
            User object does not already contain the Review
            object
            OR
            Replaces the old Review object with the new Review
            object if the User object already contains the 
            Review object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review_to_track(self, current_track: track.Track, new_review: review.Review, current_user: user.User):
        """ Adds the Review object to the Track object if the
            Track object does not already contain the Review
            object
            OR
            Replaces the old Review object with the new Review
            object if the Track object already contains the 
            Review object
        """
        raise NotImplementedError

    '''@abc.abstractmethod
    def get_user_count(self) -> int:
        """ Returns number of current users"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_reviews(self, user_name: str) -> list[review]:
        """ Returns list of reviews from user object"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_reviews(self) -> list[review]:
        """ Returns list of all reviews from repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_by_track(self, track_object: track) -> list[review]:
        """ Returns list of reviews of specific track from repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_user_review(self, user_object: user, track_object: track, review_text:str, rating: int) -> bool:
        """ Creates new user review and adds to repo/user class, returns True if done / False if cannot"""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_user_review(self, user_object: user, review_object: review):
        """ Removes user review from repo and user class"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_liked_tracks(self, user_name: str) -> list[track]:
        """ Returns list of users liked tracks from repository"""
        raise NotImplementedError

    def add_user_liked_track(self, user_name:str, track_object: track):
        """ Adds liked track to user object"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_playlists(self, user_name: str) -> list[playlist]:
        """ Returns list of user playlists"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_playlist(self, user_name: str, playlist_object: playlist) -> list[track]:
        """ Returns tracks from specific user playlist"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_playlists(self) -> list[playlist]:
        """ Returns all playlists across users --> Implement dict method if we want this"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, user_object: user, playlist_object: playlist):
        """Add playlist to User object"""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_playlist(self, user_name: str, playlist_object: playlist):
        """ Remove playlist from User object"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_playlist(self, playlist_object: playlist, track_object: track):
        """ Adds track to user playlist """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_playlist(self, playlist_object: playlist, track_object: track):
        """ Removes track from user playlist """
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist_duration(self, playlist_object: playlist):
        """ Returns total duration of playlist """
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist_size(self, playlist_object: playlist):
        """ Returns size of playlist """
        raise NotImplementedError'''

    @abc.abstractmethod
    def add_track(self, new_track: track):
        """ Adds a track to the repository"""
        if type(new_track) is not track.Track:
            raise RepositoryException("Track ID should be a non negative integer")

    @abc.abstractmethod
    def add_track_to_sort(self, new_track: track):
        """ Adds a track to the sorted list in repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_sorted_tracks(self):
        """ Returns sorted tracks list  - Only used for confirming PyTest"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, track_id: int) -> track:
        """ Returns a track with id from the repository
            If track not found, return None
        """
        raise NotImplementedError

    '''@abc.abstractmethod
    def get_tracks_by_duration(self, duration: int) -> list[track]:
        """ Returns a list of tracks with similar duration
            Duration in seconds
            Returns Empty list if no track within X seconds of duration
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_url(self, track_id: int):
        """ Returns track url of selected track
            If track or track url does not exist, return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_genres(self, track_id: int) -> list[genre]:
        """ Returns list of user reviews from repository"""
        raise NotImplementedError'''

    @abc.abstractmethod
    def get_number_of_tracks(self) -> int:
        """ Returns number of tracks in repository"""
        raise NotImplementedError

    '''@abc.abstractmethod
    def get_first_track(self) -> track:
        """ Returns first track in repository
            TBD: Order type
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self) -> track:
        """ Returns last track in repository
            TBD: Order type
        """
        raise NotImplementedError'''

    @abc.abstractmethod
    def get_list_of_tracks(self, page_start: int, songs_per_page: int) -> list[track.Track]:
        """ Returns list of tracks to display on page according to users choice of songs shown per page"""
        raise NotImplementedError

    '''@abc.abstractmethod
    def get_tracks_by_album(self, album_id: int) -> list[track]:
        """ Returns list of tracks from repository within certain album
            If no such tracks found, return empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_album(self, track_id: int) -> album:
        """ Returns album that track belongs to"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_artist(self, artist_id: int) -> list[track]:
        """ Returns list of tracks from repository by certain artist
            If no such tracks found, return empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_artist(self, track_id: int) -> artist:
        """ Returns artist that sings track"""
        raise NotImplementedError'''

    @abc.abstractmethod
    def add_album(self, new_album: album):
        """ Adds an album to the repository"""
        if type(new_album) is not album.Album:
            raise RepositoryException("Album ID should be a non negative integer")

    @abc.abstractmethod
    def get_albums(self) -> list[album.Album]:
        """ Returns albums from repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_album(self, index: int) -> album.Album:
        """ Get specific album from repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, new_artist: artist):
        """ Adds an artist to the repository"""
        if type(new_artist) is not artist.Artist:
            raise RepositoryException("Album ID should be a non negative integer")

    @abc.abstractmethod
    def get_artists(self) -> list[artist.Artist]:
        """ Returns artists from repository"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_artist(self, index: int) -> artist.Artist:
        """ Get specific artist from repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, new_genre: genre):
        """ Adds an artist to the repository"""
        if type(new_genre) is not genre.Genre:
            raise RepositoryException('Genre ID should be an integer')

    @abc.abstractmethod
    def get_genres(self) -> list[genre.Genre]:
        """ Returns genres from repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_track_dict(self, track_object: track, track_album: album, track_artist: artist):
        """ Adds track to the track dict with name, album, and artist"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_dict(self):
        """ Returns the track dict from repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def return_track_from_dict(self, input):
        """ Returns specific track from track dict"""
        raise NotImplementedError

    @abc.abstractmethod
    def sort_tracks(self, function, order: bool):
        """ Sorts tracks by user choice"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_name(self, track_obj: track):
        """ Returns track name"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_id(self, track_obj: track):
        """Returns track id"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_duration(self, track_obj: track):
        """ Returns track duration"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_artist_name(self, track_obj: track):
        """ Returns track artist name"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_album_name(self, track_obj: track):
        """ Returns track album name"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_rating(self, track_obj):
        """ Returns track rating"""
        raise NotImplementedError

    @abc.abstractmethod
    def recommend_tracks(self, user_object: user):
        """Recommends tracks to the user based on tracks they have highly reviewed"""
        raise NotImplementedError

    @abc.abstractmethod
    def recommend_from_artist(self, high_reviewed_track, track_object):
        """ Finds tracks from the same artists as ones that have been highly reviewed"""
        raise NotImplementedError

    @abc.abstractmethod
    def recommend_from_genre(self, high_reviewed_track, track_object):
        """ Finds tracks from the same genres as ones that have been highly reviewed"""
        raise NotImplementedError

    @abc.abstractmethod
    def recommend_from_album(self, high_reviewed_track, track_object):
        """ Finds tracks from the same albums as ones that have been highly reviewed"""
        raise NotImplementedError

    @abc.abstractmethod
    def recommend_from_duration(self, high_reviewed_track, track_object):
        """ Finds tracks with similar duration as ones that have been highly reviwed"""
        raise NotImplementedError

    @abc.abstractmethod
    def generate_user_id(self):
        """ returns the next available user id"""
        raise NotImplementedError

    def get_users(self):
        """ Returns list of users - Only used for confirming PyTest"""
        raise NotImplementedError

    class UsernameInUse(Exception):
        pass

    class UnknownUserException(Exception):
        pass

    class AuthenticationException(Exception):
        pass

    class TrackAlreadyReviewed(Exception):
        pass