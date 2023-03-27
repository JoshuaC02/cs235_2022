import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel import album, artist, genre, review, track, user


def test_loading_of_user(empty_session):
    empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                        {'id': 3,'user_name': "test", 'password': "Password1"})

    assert empty_session.query(user.User).all()[0].user_name == "test"


def test_saving_of_users(empty_session):
    empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                        {'id': 4,'user_name': "test", 'password': "Password1"})
    
    assert len(list(empty_session.execute('SELECT user_name, password FROM users'))) != 0


def test_saving_of_users_with_common_id(empty_session):
    empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                        {'id': 4,'user_name': "test", 'password': "Password1"})

    with pytest.raises(IntegrityError):
        empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                        {'id': 5,'user_name': "test", 'password': "Password1"})


def test_loading_of_track(empty_session):
    track_obj = track.Track(999, "test_track")
    track_obj.album = album.Album(999, "test_album")
    track_obj.artist = artist.Artist(999, "test_artist")
    track_obj.track_duration = 5
    track_obj.track_url = "www.google.com"
    track_key = empty_session.execute('INSERT INTO tracks (id, title, album_id, artist_id, duration, track_url) VALUES (999, "test_track", 999, 999, 5, "www.google.com")')
    expected_track = track_obj
    fetched_track = empty_session.query(track.Track).one()

    assert expected_track == fetched_track


def test_loading_of_reviewed_track(empty_session):
    # Create Track User objects.
    track_obj = track.Track(999, "test_track")
    track_obj.album = album.Album(999, "test_album")
    track_obj.artist = artist.Artist(999, "test_artist")
    track_obj.track_duration = 5
    track_obj.track_url = "www.google.com"
    user_obj = user.User(999, "test_user", "testPassword1")

    review_text = "review_text"
    review_obj = review.Review(track_obj, review_text, 5, user_obj)

    empty_session.add(track_obj)
    empty_session.commit()

    rows = empty_session.query(track.Track).all()
    tracks = rows[0]

    for reviews in tracks.reviews:
        assert reviews.track is track_obj


def test_saving_of_review(empty_session):
    track_obj = track.Track(999, "test_track")
    track_obj.album = album.Album(999, "test_album")
    track_obj.artist = artist.Artist(999, "test_artist")
    track_obj.track_duration = 5
    track_obj.track_url = "www.google.com"
    user_obj = user.User(999, "test_user", "testPassword1")
    review_obj = review.Review(track_obj, "review text", 5, user_obj)
    empty_session.add(review_obj)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, user_id, track_id, review, rating FROM reviews'))
    assert rows == [(1, 999, 999, "review text", 5)]


def test_saving_of_track(empty_session):
    track_obj = track.Track(999, "test_track")
    track_obj.album = album.Album(999, "test_album")
    track_obj.artist = artist.Artist(999, "test_artist")
    track_obj.track_duration = 5
    track_obj.track_url = "www.google.com"
    empty_session.add(track_obj)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, title, album_id, artist_id, duration, track_url FROM tracks'))
    assert rows == [(999, "test_track", 999, 999, 5, "www.google.com")]


def test_save_reviewed_track(empty_session):
    # Create Track User objects.
    track_obj = track.Track(999, "test_track")
    track_obj.album = album.Album(999, "test_album")
    track_obj.artist = artist.Artist(999, "test_artist")
    track_obj.track_duration = 5
    track_obj.track_url = "www.google.com"
    user_obj = user.User(999, "test_user", "testPassword1")

    # Create a new Review that is bidirectionally linked with the User and Track.
    review_text = "review_text"
    review_obj = review.Review(track_obj, review_text, 5, user_obj)

    # Save the new Track.
    empty_session.add(track_obj)
    empty_session.commit()

    # Test test_saving_of_track() checks for insertion into the tracks table.
    rows = list(empty_session.execute('SELECT id FROM tracks'))
    track_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, track_id, review FROM reviews'))
    assert rows == [(user_key, track_key, review_text)]
