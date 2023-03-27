import csv, ast, random
from datetime import datetime
from pathlib import Path

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel import album, artist, genre, playlist, review, track, user

def read_csv_file(filename: str):
        with open(filename, encoding="unicode_escape") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                row = [item.strip() for item in row]
                yield row

def load_tracks(data_path: Path, repo: AbstractRepository):
    pass
    """
    tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    for row in read_csv_file(tracks_filename):
        if row[0] == "track_id":
            continue
        track_name_fixed = row[37].replace('&amp;', '&')
        new_track = track.Track(int(row[0]), track_name_fixed)
        if row[1] == "":
            pass
        else:
            album_name_fixed = row[2].replace('&amp;', '&')
            new_track.album = album.Album(int(row[1]), album_name_fixed)
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
        """

def load_albums(data_path: Path, repo: AbstractRepository):
    albums_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    repo.add_album(album.Album(0, "None"))
    for row in read_csv_file(albums_filename):
        if row[0] == "track_id":
            continue
        elif row[1] == "":
            continue
        album_name_fixed = row[2].replace('&amp;', '&')
        new_album = album.Album(int(row[1]), album_name_fixed)
        new_album.album_url = row[3]
        unique_flag = True
        album_list = repo.get_albums()
        for check_album in album_list:
            if check_album.album_id == new_album.album_id:
                unique_flag = False
        if unique_flag:
            repo.add_album(new_album)

    """
    albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
    repo.add_album(album.Album(0, "None"))
    for row in read_csv_file(albums_filename):
        if row[0] == "album_id":
            continue
        album_name_fixed = row[12].replace('&amp;', '&')
        new_album = album.Album(int(row[0]), album_name_fixed)
        if row[15] == None:
            new_album.album_url = 'None'
        else:
            new_album.album_url = row[15]
        if row[14] == None:
            new_album.album_type = "None"
        else: 
            new_album.album_type = row[14]
        if row[3] == "":
            new_album.release_year = 0
        else:
            new_album.release_year = int(row[3])
        album_list = repo.get_albums()
        unique_flag = True
        for check_album in album_list:
            if check_album.album_id == new_album.album_id:
                unique_flag = False
        if unique_flag:
            repo.add_album(new_album)
    """


def load_artists(data_path: Path, repo: AbstractRepository):
    artists_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    artist_id_list = []
    for row in read_csv_file(artists_filename):
        if row[0] == "track_id":
            continue
        if row[4] in artist_id_list:
            continue
        else:
            artist_id_list.append(row[4])
        artist_name_fixed = row[5].replace('&amp;', '&')
        new_artist = artist.Artist(int(row[4]), artist_name_fixed)
        artist_list = repo.get_artists()
        unique_flag = True
        for check_artist in artist_list:
            if check_artist.artist_id == new_artist.artist_id:
                unique_flag = False
        if unique_flag:
            repo.add_artist(new_artist)


def load_genres(data_path: Path, repo: AbstractRepository, database_mode: bool = False):
    genres_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    for row in read_csv_file(genres_filename):
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
            repo_genre_list = repo.get_genres()
            unique_flag = True
            for check_genre in repo_genre_list:
                if check_genre.genre_id == new_genre.genre_id:
                    unique_flag = False
            if unique_flag:
                new_genre.apply_to(new_track)
                repo.add_genre(new_genre)
            else:
                for loop_genre in repo_genre_list:
                    if loop_genre.genre_id == new_genre.genre_id:
                        loop_genre.apply_to(new_track)

def load_tracks_and_genres(data_path: Path, repo: AbstractRepository):
    # First, create Tracks
    tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    genre_list = []
    for row in read_csv_file(tracks_filename):
        if row[0] == "track_id":
            continue
        track_name_fixed = row[37].replace('&amp;', '&')
        new_track = track.Track(int(row[0]), track_name_fixed)
        new_track.track_url = row[38]
        new_track.track_duration = int(float(row[22]))
        check_artist = repo.get_artist(int(row[4]))
        new_track.artist = check_artist
        check_album = None
        if row[1] == "":
            check_album = repo.get_album(0)
        else:
            check_album = repo.get_album(int(row[1]))
        new_track.album = check_album
        """
        for check_artist in artist_list:
            if check_artist.artist_id == int(row[4]):
                new_track.artist = check_artist
                break
        if row[1] == "":
            check_album = repo.get_albums()[0]
            new_track.album = check_album
        else:
            for check_album in album_list:
                if check_album.album_id == int(row[1]):
                    new_track.album = check_album
                    break
        """
        if row[27] != "":
            for genre_object in ast.literal_eval(row[27]):
                # Here, we check to see if the genres are unique
                unique_flag = True
                for check_genre in genre_list:
                    if check_genre.genre_id == int(genre_object["genre_id"]):
                        new_track.add_genre(check_genre)
                        unique_flag = False
                if unique_flag:
                    new_genre = genre.Genre(int(genre_object["genre_id"]), genre_object["genre_title"])
                    repo.add_genre(new_genre)
                    new_track.add_genre(new_genre)
                    genre_list.append(new_genre)
                    

        check_album.add_track(new_track)
        check_artist.add_track(new_track)
        repo.add_track(new_track)
        
        #repo.add_track_to_sort(new_track)
        #repo.add_track_dict(new_track, new_track.album, new_track.artist)

def populate(data_path: Path, repo: AbstractRepository):
    #Primary way, will return to later
    #load_all(data_path, repo)

    #Interesting fix
    load_albums(data_path, repo)
    load_artists(data_path, repo)
    load_tracks_and_genres(data_path, repo)
    
    #depreciation functions
    #load_tracks(data_path, repo)
    #load_genres(data_path, repo)


def load_all(data_path: Path, repo: AbstractRepository):
    tracks_filename = str(Path(data_path) / "raw_tracks_excerpt.csv")
    albums_filename = str(Path(data_path) / "raw_albums_excerpt.csv")
    album_list = [album.Album(0, "None")]
    artist_list = []

    #First, initalise album_list
    for row in read_csv_file(albums_filename):
        if row[0] == "album_id":
            continue
        album_name_fixed = row[12].replace('&amp;', '&')
        new_album = album.Album(int(row[0]), album_name_fixed)
        if row[15] == None:
            new_album.album_url = 'None'
        else:
            new_album.album_url = row[15]
        new_album.album_type = row[14]
        if row[3] == "":
            new_album.release_year = 0
        else:
            new_album.release_year = int(row[3])
        unique_flag = True
        for check_album in album_list:
            if check_album.album_id == new_album.album_id:
                unique_flag = False
        if unique_flag:
            album_list.append(new_album)
    print(album_list)
    #Secondly, initalise artist_list
    for row in read_csv_file(tracks_filename):
        if row[0] == "track_id":
            continue
        artist_name_fixed = row[5].replace('&amp;', '&')
        new_artist = artist.Artist(int(row[4]), artist_name_fixed)
        unique_flag = True
        for check_artist in artist_list:
            if check_artist.artist_id == new_artist.artist_id:
                unique_flag = False
        if unique_flag:
            artist_list.append(new_artist)
    print(artist_list)
    #Finally, create the track objects, complete with their cooresponding album and artist
    # Remember to include checks if artist/album in repo

    for row in read_csv_file(tracks_filename):
        if row[0] == "track_id":
            continue
        track_name_fixed = row[37].replace('&amp;', '&')
        new_track = track.Track(int(row[0]), track_name_fixed)
        new_track.track_url = row[38]
        new_track.track_duration = int(float(row[22]))
        print(new_track, len(album_list), len(artist_list))

        #SET TRACK ALBUM
        #Search through album_list for album
        for index in range(len(album_list)-1):
            if album_list[index].album_id == int(row[1]):
                print("Unique ID found!")
                new_track.album = album_list[index]
                album_list.pop(index)
        #If nothing, it means it either doesn't have an album, or it's already in repo
        if new_track.album.album_id == 0:
            print("Searching DB, potentially null")
            #check to see if it has an album
            if row[1] == "":
                print("It's null")
                #check to see if default album still in album_list
                if album_list[0].album_id != 0:
                    for check_album in repo.get_albums():
                        if check_album.album_id == 0:
                            check_album.add_track(new_track)
                else:
                    new_track.album = album_list[0]
                    album_list.pop(0)
            else:
            #check to see if it's in repo
                for check_album in repo.get_albums():
                    if check_album.album_id == int(row[1]):
                        check_album.add_track(new_track)
                        print(new_track.album, "NEW_TRACK")
            
        #SET TRACK ARTIST
        for index in range(len(artist_list)-1):
            if artist_list[index].artist_id == int(row[4]):
                new_track.artist = artist_list[index]
                artist_list.pop(index)
        if new_track.artist.artist_id == 0:
            for check_artist in repo.get_artists():
                print(check_artist, int(row[4]))
                if check_artist.artist_id == int(row[4]):
                    check_artist.add_track(new_track)
                    #new_track.artist = check_artist

        
        
        if row[27] != "":
            for genre_object in ast.literal_eval(row[27]):
                # Here, we check to see if the genres are unique
                unique_flag = True
                for check_genre in repo.get_genres():
                    if check_genre.genre_id == int(genre_object["genre_id"]):
                        new_track.add_genre(check_genre)
                        unique_flag = False
                if unique_flag:
                    new_genre = genre.Genre(int(genre_object["genre_id"]), genre_object["genre_title"])
                    new_track.add_genre(new_genre)
        repo.add_track(new_track)

#Keep as old code
"""
if row[1] == "":
    for check_album in repo.get_albums():
        if check_album.album_id == 0:
            new_track.album = check_album
    if new_track.album == None:
        new_album = album.Album(0, "None")
        new_album.album_url = "N/A"
        new_album.album_type = "N/A"
        new_album.release_year = 0
        new_track.album = new_album
else:
    for new_album in repo.get_albums():
        if new_album.album_id == int(row[1]):
            new_track.album = new_album
    #album_name_fixed = row[2].replace('&amp;', '&')
    #new_track.album = album.Album(int(row[1]), album_name_fixed)
for new_artist in repo.get_artists():
    if new_artist.artist_id == int(row[4]):
        new_track.artist = new_artist
#artist_name_fixed = row[5].replace('&amp;', '&')
#new_track.artist = artist.Artist(int(row[4]), artist_name_fixed)
"""