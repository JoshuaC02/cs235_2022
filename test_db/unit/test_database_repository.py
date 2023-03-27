from datetime import datetime, date

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel import album, artist, genre, review, track, user
from music.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_user = user.User(repo.generate_user_id(), 'Dave', 'Password1')
    repo.add_user(new_user)

    repo.add_user(user.User(repo.generate_user_id(), 'Martin', 'Password1'))

    get_user = repo.get_user('Dave')

    assert get_user == new_user and get_user is new_user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    repo.add_user(user.User(repo.generate_user_id(), 'Martin', 'Password1'))

    get_user = repo.get_user('Martin')

    assert get_user.user_name == 'Martin'

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('Prince')
    assert user is None

def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = repo.get_number_of_tracks()

    # Check that the query returned 2000 Tracks.
    assert number_of_tracks == 2000

def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_track = track.Track(1, 'some_title')
    new_track.track_duration = 1
    repo.add_track(new_track)

    assert repo.get_track(1) == new_track

def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_track = track.Track(1, 'some_title')
    new_track.track_duration = 1
    repo.add_track(new_track)

    get_track = repo.get_track(1)
    
    assert get_track == new_track and get_track.title == 'some_title' and get_track.track_id == 1 and get_track.track_duration == 1

def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_track(1)
    assert article is None

def test_repository_can_retrieve_tracks_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    repo.sort_tracks("get_track_artist_name", False)

    tracks = repo.get_list_of_tracks(1, 1)

    first_track = tracks[0]

    assert first_track.artist.full_name == "??ss"

def test_repository_can_retrieve_tags(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 60

    genre_one = [get_genre for get_genre in genres if get_genre.name == 'Jazz'][0]
    genre_two = [get_genre for get_genre in genres if get_genre.name == 'Pop'][0]
    genre_three = [get_genre for get_genre in genres if get_genre.name == 'Disco'][0]
    genre_four = [get_genre for get_genre in genres if get_genre.name == 'Rock'][0]

    assert len(genre_one.get_applied_to()) == 31
    assert len(genre_two.get_applied_to()) == 40
    assert len(genre_three.get_applied_to()) == 42
    assert len(genre_four.get_applied_to()) == 542

def test_repository_can_get_first_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(2)
    assert track.title == 'Food'

def test_repository_can_get_last_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_all_tracks()
    track = tracks[-1]
    assert track.title == 'yet to be titled'

def test_repository_can_get_tracks_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track_1 = repo.get_track(2)
    track_2 = repo.get_track(3)
    track_3 = repo.get_track(5)

    assert isinstance(track_1, track.Track) and isinstance(track_2, track.Track) and isinstance(track_3, track.Track)
    assert track_1.title == 'Food'
    assert track_2.title == 'Electric Ave'
    assert track_3.title == 'This World'

def test_repository_does_not_retrieve_article_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = [repo.get_track(1), repo.get_track(2)]

    assert tracks[0] == None
    assert tracks[1].title == 'Food'

def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_genre = genre.Genre(2000, 'Motoring')
    repo.add_genre(new_genre)

    assert new_genre in repo.get_genres()

def test_repository_can_add_a_review_and_retrieve_from_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_user = user.User(repo.generate_user_id(), "test", "Password1")
    repo.add_user(new_user)
    new_track = repo.get_track(2)
    new_review = review.Review(new_track, "test", 4, new_user)
    repo.add_review(new_review)
    new_track.add_review(new_review)

    assert new_review in repo.get_track(2).reviews

def test_can_retrieve_a_track_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Article and User.
    new_track = repo.get_track(2)
    new_user = user.User(repo.generate_user_id(), "test", "Password1")
    repo.add_user(new_user)

    # Create a new Comment, connecting it to the Article and User.
    new_review = review.Review(new_track, "test", 5, new_user)
    repo.add_review(new_review)
    new_user.add_review(new_review)
    new_track.add_review(new_review)


    article_fetched = repo.get_track(2)
    author_fetched = repo.get_user('test')

    assert new_review in article_fetched.reviews
    assert new_review in author_fetched.reviews

def test_recommend_does_not_return_none(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    new_user = user.User(repo.generate_user_id(), "test", "Password1")
    repo.add_user(new_user)
    new_track = repo.get_track(2)
    new_review = review.Review(new_track, "test", 5, new_user)
    repo.add_review(new_review)
    new_track.add_review(new_review)
    new_user.add_review(new_review)

    output = repo.recommend_tracks(new_user)

    assert len(output) != 0