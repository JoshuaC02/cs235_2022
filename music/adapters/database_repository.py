from datetime import date
from typing import List
import csv, ast, random
from pathlib import Path

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from music.browse.services import get_list_of_tracks 

from music.domainmodel import album, artist, genre, playlist, review, track, user
from music.adapters.repository import AbstractRepository
from music.adapters import orm
from music.adapters.memory_repository import MemoryRepository

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def flush(self):
        self.__session.flush()

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        #self._sorted_tracks = []

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def update_tracks(self):
        table = self._session_cm.session.query(track.Track)
        data_path = Path('music') / 'adapters' / 'data'
        tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
        for track_obj in table:
            for row in self.read_csv_file(tracks_filename):
                if int(row[0]) == track_obj.track_id:
                    current_artist_id = row[4]
                    current_album_id = row[1]
                    self._session_cm.session.execute(f"UPDATE tracks SET artist_id = '{current_artist_id}', album_id = '{current_album_id}' WHERE id='{track_obj.track_id}'")
                    self._session_cm.session.execute(f"UPDATE tracks SET album_id = '{current_album_id}' WHERE id='{track_obj.track_id}'")
        self._session_cm.session.commit()
        self._session_cm.session.close()

    def get_sorted_list(self, method, order):
        sql = f"""  
                SELECT *
                FROM tracks
                LEFT OUTER JOIN artists
                ON artist.id = track.artist_id
                LEFT OUTER JOIN albums
                ON album.id = track.album_id
                RIGHT OUTER JOIN reviews
                ON reviews.track_id = track.id
                ORDER BY {method} {order}
                """
        x = self._session_cm.session.execute(sql)
        return x.fetchall()

        # in order to allow for sort by artist name for example, need:

    def get_artist_by_id(self, id):
        return_name = None
        try:
            return_name = (self._session_cm.session.query(artist.Artist).filter(artist.Artist.artist_id == id)).artist_name
        except:pass
        return return_name

    def get_album_by_id(self,id):
        return_name = None
        try:
            return_name = (self._session_cm.session.query(album.Album).filter(album.Album.album_id == id)).album_name
        except:
            pass
        return return_name

    def read_csv_file(self, filename: str):
        with open(filename, encoding="unicode_escape") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                row = [item.strip() for item in row]
                yield row

    def add_user(self, new_user: user.User):
        with self._session_cm as scm:
            scm.session.add(new_user)
            scm.commit()

    def get_user(self, user_name: str):
        return_user = None
        try:
            return_user = self._session_cm.session.query(user.User).filter(user.User._User__user_name == user_name).one()
        except:
            return_user = None
        return return_user

    def add_review(self, new_review: review.Review):
        sql = f"""
                            SELECT id
                            FROM reviews
                            WHERE reviews.user_id == {new_review.review_user.user_id}
                            AND reviews.track_id == {new_review.track.track_id}
                            """
        x = self._session_cm.session.execute(sql)
        y = (x.fetchall())
        if len(y) > 1:
            sql = f"""
                UPDATE reviews
                SET review = '{new_review.review_text}', rating = {new_review.rating}
                WHERE user_id = {new_review.review_user.user_id} AND track_id = {new_review.track.track_id}
                """
            self._session_cm.session.execute(sql)
            self._session_cm.session.commit()

            remove_id = len(self._session_cm.session.query(review.Review).all())
            sql = f"""
                DELETE FROM reviews
                WHERE reviews.id = {remove_id}
                """
            self._session_cm.session.execute(sql)
            self._session_cm.session.commit()
        else:
            self._session_cm.session.add(new_review)
            self._session_cm.session.commit()








    def get_track_reviews(self, track_id: int):
        return_reviews = None
        try:
            return_reviews = self._session_cm.session.query(review.Review).filter(review.Review._Review__track.track_id == track_id).all()
        except:pass
        return return_reviews

    def add_review_to_user(self, user: user.User, review: review.Review):
        flag = True
        for old_review in range(len(user.reviews)): # check if review is in user obj
            if user.reviews[old_review].track.track_id == review.track.track_id:
                flag = False
                #user.reviews[old_review] = review # replace if review is in user obj
                break
        if flag:
            pass
            user.add_review(review)
        self.add_review(review)

    def add_review_to_track(self, track: track.Track, review: review.Review, user: user.User):
        flag = True
        for old_track in range(len(track.reviews)): # check if review is in track obj
            if track.reviews[old_track].review_user == user:
                flag = False
                track.reviews[old_track] = review # replace if review is in track obj
                break
        if flag:
            pass
            track.add_review(review)
            
            

    def add_track(self, track: track.Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()
    
    def add_track_to_sort(self, track: track.Track):
        #depreciated function, not used for the database 
        pass

    def get_sorted_tracks(self):
        pass
        #return self._sorted_tracks
    
    def get_track(self, track_id: int):
        return_track = None
        try:
            return_track = self._session_cm.session.query(track.Track).filter(track.Track._Track__track_id == track_id).one()
        except:
            return_track = None
        return return_track

    def get_number_of_tracks(self) -> int:
        return len(self._session_cm.session.query(track.Track).all())

    def get_all_tracks(self) -> list:
        return self._session_cm.session.query(track.Track).all()

    def get_list_of_tracks(self, page_start: int, songs_per_page: int) -> list[track.Track]:
        #list = self._session_cm.session.query(track.Track).order_by(track.Track._Track__title)
        sql = "SELECT * from sort_track"
        get_tracks = self._session_cm.session.execute(sql)
        tracks = get_tracks.fetchall()
        if tracks == []:
            self.sort_tracks("get_track_id", False)
        else:
            sorted_tracks = []
            first_track = (page_start - 1) * songs_per_page
            last_track = first_track + songs_per_page
            wanted_tracks = tracks[first_track:last_track]
            for new_track in wanted_tracks:
                sorted_tracks.append(self.get_track(new_track[1]))
            return sorted_tracks

    def add_album(self, album: album.Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()

    def get_albums(self) -> list[album.Album]:
        album_list = self._session_cm.session.query(album.Album).all()
        return album_list
    
    def get_album(self, index: int) -> album.Album:
        try:
            return self._session_cm.session.query(album.Album).filter(album.Album._Album__album_id == index).one()
        except:
            return None

    def add_artist(self, artist: artist.Artist):
        with self._session_cm as scm:
            scm.session.add(artist)
            scm.commit()

    def get_artists(self) -> list[artist.Artist]:
        artist_list = self._session_cm.session.query(artist.Artist).all()
        return artist_list
    
    def get_artist(self, index: int) -> artist.Artist:
        return self._session_cm.session.query(artist.Artist).filter(artist.Artist._Artist__artist_id == index).one()

    def add_genre(self, genre: genre.Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genres(self) -> list[genre.Genre]:
        genre_list = self._session_cm.session.query(genre.Genre).all()
        return genre_list


    def add_track_dict(self, track_object: track.Track, track_album: album.Album, track_artist: artist.Artist):
        #depreciated function, not used for the database 
        pass

    def get_track_dict(self):
        return self._session_cm.session.query(track.Track).all()

    def return_track_from_dict(self, input):
        sql = f"""
                    SELECT tracks.id, tracks.title, albums.id, albums.title, artists.id, artists.full_name, tracks.duration
                    FROM tracks
                    LEFT OUTER JOIN albums
                    ON tracks.album_id = albums.id
                    LEFT OUTER JOIN artists
                    ON tracks.artist_id = artists.id
                    WHERE tracks.title LIKE '%{input}%' OR albums.title LIKE '%{input}%' OR artists.full_name LIKE '%{input}%'
                    """
        sql2 = f"""  
                    SELECT *
                    FROM reviews
                    LEFT OUTER JOIN users
                    ON reviews.user_id = users.id
                    """
        x = self._session_cm.session.execute(sql)
        return_list = []
        for tup in x.fetchall():
            newTrack = track.Track(int(tup[0]), tup[1])
            newTrack.album = album.Album(int(tup[2]), tup[3])
            newTrack.artist = artist.Artist(int(tup[4]), tup[5])
            newTrack.track_duration = int(tup[6])
            return_list.append(newTrack)
        review_sql = self._session_cm.session.execute(sql2)
        for obj in review_sql.fetchall():
            for track_obj in return_list:
                if track_obj.track_id == int(obj[2]):
                    newReview = review.Review(track_obj, obj[3], int(obj[4]), user.User(int(obj[1]), obj[7], obj[8]))
        return return_list
        #for track_obj in self._session_cm.session.query(track.Track).all():
        #    check_list = [track_obj.title, track_obj.artist.full_name, track_obj.album.title]
        #    for item in check_list:
        #        if input in item.lower():
        #            return_list.append(track_obj)
        #            if len(return_list) == 30:
        #                return return_list


    def sort_tracks(self, function: str, order: bool):
        return_list = []
        if order == True:
            updown = "DESC"
        else:
            updown = "ASC"
        if function == "get_track_name":
            func = "tracks.title"
        elif function == "get_track_id":
            func = "tracks.id"
        elif function == "get_track_duration":
            func = "tracks.duration"
        elif function == "get_track_artist_name":
            func = "artists.full_name"
        elif function == "get_track_album_name":
            func = "albums.title"
        elif function == "get_track_rating":
            func = "(reviews.rating)"
        
        sql = f"""  
            SELECT *
            FROM tracks
            LEFT OUTER JOIN artists
            ON artists.id = tracks.artist_id
            LEFT OUTER JOIN albums
            ON albums.id = tracks.album_id
            LEFT OUTER JOIN reviews 
            ON reviews.track_id = tracks.id
            ORDER BY {func} {updown}
            """
        x = self._session_cm.session.execute(sql)
        delete = "DELETE FROM sort_track"
        self._session_cm.session.execute(delete)
        temp_track_list = []
        for obj in x.fetchall():
            number = int(obj[0])
            if number not in temp_track_list:
                temp_track_list.append(number)
                insert = f"INSERT INTO sort_track (track_id) VALUES ({number})"
                self._session_cm.session.execute(insert)
        self._session_cm.session.commit()

        #get_tracks = self._session_cm.session.query(track.Track).all()
        

        #sql = f"""  
        #    SELECT *
        #    FROM tracks
        #    LEFT OUTER JOIN artists
        #    ON artists.id = tracks.artist_id
        #    LEFT OUTER JOIN albums
        #    ON albums.id = tracks.album_id
        #    ORDER BY {func} {updown}
        #    """
        #sql2 = f"""  
        #    SELECT *
        #    FROM reviews
        #    LEFT OUTER JOIN users
        #    ON reviews.user_id = users.id
        #    """
        #x = self._session_cm.session.execute(sql)
        #for obj in x.fetchall():
        #    newTrack = track.Track(int(obj[0]), obj[1])
        #    newTrack.track_duration = obj[4]
        #    newTrack.artist = artist.Artist(int(obj[6]), obj[7])
        #    try:
        #        newTrack.album = album.Album(int(obj[8]), obj[9])
        #    except:
        #        newTrack.album = album.Album(0, "None")
        #    return_list.append(newTrack)
        #review_sql = self._session_cm.session.execute(sql2)
        #for obj in review_sql.fetchall():
        #    for track_obj in return_list:
        #        if track_obj.track_id == int(obj[2]):
        #            newReview = review.Review(track_obj, obj[3], int(obj[4]), user.User(int(obj[1]), obj[7], obj[8]))
        #            #track_obj.add_review(newReview)
        #self._sorted_tracks = return_list

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
        high_reviewed_tracks = []
        tracks_list = []
        self.recommended_tracks = []
        sql = f"""  
                        SELECT *
                        FROM tracks
                        LEFT OUTER JOIN artists
                        ON artists.id = tracks.artist_id
                        LEFT OUTER JOIN albums
                        ON albums.id = tracks.album_id
                        """
        sql2 = f"""  
                        SELECT *
                        FROM reviews
                        LEFT OUTER JOIN users
                        ON users.id = reviews.user_id
                        """
        track_sql = self._session_cm.session.execute(sql)
        for obj in track_sql.fetchall():
            newTrack = track.Track(int(obj[0]), obj[1])
            newTrack.track_duration = obj[4]
            newTrack.artist = artist.Artist(int(obj[6]), obj[7])
            try:
                newTrack.album = album.Album(int(obj[8]), obj[9])
            except:
                newTrack.album = album.Album(0, "None")

            tracks_list.append(newTrack)
        review_sql = self._session_cm.session.execute(sql2)
        for obj in review_sql.fetchall():
            for track_obj in tracks_list:
                if track_obj.track_id == int(obj[2]):
                    newReview = review.Review(track_obj, obj[3], int(obj[4]), user.User(int(obj[1]), obj[7], obj[8]))
                    if obj[4] > 3 and obj[1] == user_object.user_id:
                        high_reviewed_tracks.append(track_obj)
        for high_reviewed_track in high_reviewed_tracks:
            for track_obj in tracks_list:
                self.recommend_from_artist(high_reviewed_track, track_obj)
                self.recommend_from_genre(high_reviewed_track, track_obj)
                self.recommend_from_album(high_reviewed_track, track_obj)
                self.recommend_from_duration(high_reviewed_track, track_obj)
        random.shuffle(self.recommended_tracks)
        if len(self.recommended_tracks) > 10:
            self.recommended_tracks = self.recommended_tracks[0:10]
        return self.recommended_tracks
    
    def recommend_from_artist(self, high_reviewed_track, track_object):
        if high_reviewed_track.artist == track_object.artist and high_reviewed_track != track_object and track_object not in self.recommended_tracks:
            self.recommended_tracks.append(track_object)

    def recommend_from_genre(self, high_reviewed_track, track_object):
        for genre_type in high_reviewed_track.genres:
            if genre_type in track_object.genres and high_reviewed_track != track_object and track_object not in self.recommended_tracks:
                self.recommended_tracks.append(track_object)

    def recommend_from_album(self, high_reviewed_track, track_object):
        if high_reviewed_track.album == track_object.album and high_reviewed_track != track_object and track_object not in self.recommended_tracks:
            self.recommended_tracks.append(track_object)
    
    def recommend_from_duration(self, high_reviewed_track, track_object):
        if high_reviewed_track.track_duration-15 <= track_object.track_duration <= high_reviewed_track.track_duration+15 and high_reviewed_track != track_object and track_object not in self.recommended_tracks:
            self.recommended_tracks.append(track_object)

    def generate_user_id(self) -> int:
        return len(self.get_users())

    def get_users(self):
        return self._session_cm.session.query(user.User).all()