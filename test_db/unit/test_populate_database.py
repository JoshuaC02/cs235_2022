from sqlalchemy import select, inspect
from datetime import datetime, date

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel import album, artist, genre, review, track, user
from music.adapters.repository import RepositoryException
from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums', 'artists', 'genres', 'reviews', 'sort_track', 'track_genre', 'tracks', 'users']

def test_database_populate_select_all_albums(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_albums_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table albums
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_albums = []
        for row in result:
            all_albums.append((row['id'], row['title']))

        nr_albums = len(all_albums)
        assert nr_albums == 432

        assert all_albums[1] == (1, 'AWOL - A Way Of Life')

def test_database_populate_select_all_artists(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_artists_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table artists
        select_statement = select([metadata.tables[name_of_artists_table]])
        result = connection.execute(select_statement)

        all_artists = []
        for row in result:
            all_artists.append((row['id'], row['full_name']))

        nr_artists = len(all_artists)
        assert nr_artists == 263
        assert all_artists[0] == (1, 'AWOL')

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append((row['id'], row['genre_name']))

        nr_genres = len(all_genres)
        assert nr_genres == 60
        assert all_genres[0] == (1, 'Avant-Garde')

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[3]
    with database_engine.connect() as connection:
        # query for records in table reviews
        connection.execute(f"INSERT INTO {name_of_reviews_table} (id, user_id, track_id, review, rating) VALUES ('999', '999', '999', 'TEST REVIEW', '5')")
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)
        all_reviews = []
        for row in result:
            all_reviews.append((row['rating'], row['review']))

        assert all_reviews[-1] == (5, "TEST REVIEW")

def test_database_populate_select_all_track_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_track_genres_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table track_genres
        select_statement = select([metadata.tables[name_of_track_genres_table]])
        result = connection.execute(select_statement)

        all_track_genres = []
        for row in result:
            all_track_genres.append((row['id'], row['track_id']))

        nr_track_genres = len(all_track_genres)
        assert nr_track_genres == 2268
        assert all_track_genres[0] == (1, 2)

def test_database_populate_select_all_tracks(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[6]


    with database_engine.connect() as connection:
        # query for records in table tracks
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['id'], row['title']))

        nr_tracks = len(all_tracks)
        assert nr_tracks == 2000
        assert all_tracks[0] == (2, 'Food')

def test_database_populate_select_all_users(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[7]
    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        connection.execute(f"INSERT INTO {name_of_users_table} (id, user_name, password) VALUES ('999', 'test_user', 'testPassword1')")
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users[0] == "test_user"