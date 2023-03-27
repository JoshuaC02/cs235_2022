import pytest
from flask import session
from music.domainmodel import album, artist, genre, review, track, user
from music.authentication import services as auth_services
from music.browse import services as browse_services
from tests_mem.conftest import auth, in_memory_repo


def test_can_create_and_add_user(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'

    auth_services.create_and_add_user(username, password, in_memory_repo)

    retrieved_user = auth_services.get_user(username, in_memory_repo)

    assert retrieved_user.user_name == username

    assert retrieved_user.password.startswith('pbkdf2:sha256:')

def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'

    auth_services.create_and_add_user(username, password, in_memory_repo)

    with pytest.raises(auth_services.UsernameInUse):
        auth_services.create_and_add_user(username, password, in_memory_repo)

def test_authentication_with_valid_credentials(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'

    auth_services.create_and_add_user(username, password, in_memory_repo)

    try:
        auth_services.authenticate_user(username, password, in_memory_repo)
    except auth_services.AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'

    auth_services.create_and_add_user(username, password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.sign_in(session, username, 'abcdefgh', in_memory_repo)

def test_can_create_review(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'
    auth_services.create_and_add_user(username, password, in_memory_repo)

    user = auth_services.get_user(username, in_memory_repo)

    track = browse_services.get_track(3, in_memory_repo)
    comment = "epic music!"
    rating = 4

    new_review = browse_services.create_review(track, comment, rating, user)

    assert isinstance(new_review, review.Review) == True

def test_cannot_create_review(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'
    auth_services.create_and_add_user(username, password, in_memory_repo)

    user = auth_services.get_user(username, in_memory_repo)

    track = browse_services.get_track(3, in_memory_repo)
    comment = "epic music!"
    rating = 6
    
    with pytest.raises(ValueError):
        new_review = browse_services.create_review(track, comment, rating, user)

def test_can_add_review_to_user(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'
    auth_services.create_and_add_user(username, password, in_memory_repo)

    user = auth_services.get_user(username, in_memory_repo)

    track = browse_services.get_track(3, in_memory_repo)
    comment = "epic music!"
    rating = 4

    new_review = browse_services.create_review(track, comment, rating, user)

    browse_services.add_review_to_user(user, new_review, in_memory_repo)

    assert user.reviews[0] == new_review

def test_can_add_review_to_track(in_memory_repo):
    username = 'abcd'
    password = 'Abcdefg1'
    auth_services.create_and_add_user(username, password, in_memory_repo)

    user = auth_services.get_user(username, in_memory_repo)

    track = browse_services.get_track(3, in_memory_repo)
    comment = "epic music!"
    rating = 4

    new_review = browse_services.create_review(track, comment, rating, user)

    browse_services.add_review_to_track(track, new_review, user, in_memory_repo)

    assert track.reviews[0] == new_review

def test_can_get_track(in_memory_repo):
    track_id = 2

    track = browse_services.get_track(track_id, in_memory_repo)

    assert track.track_id == 2
    assert track.title == "Food"
    assert track.artist.full_name == "AWOL"
    assert track.album.title == "AWOL - A Way Of Life"
    assert track.track_duration == 168
    assert len(track.reviews) == 0

def test_cannot_get_track(in_memory_repo):
    track_id = 1

    track = browse_services.get_track(track_id, in_memory_repo)

    assert track == None

def test_get_first_page_of_tracks(in_memory_repo):
    first_page = browse_services.get_list_of_tracks(1, 30, in_memory_repo)

    first_track = browse_services.get_track(2, in_memory_repo)
    last_track = browse_services.get_track(155, in_memory_repo)

    assert first_page[0] == first_track
    assert first_page[29] == last_track

def test_can_get_reviews_for_track(in_memory_repo):
    auth_services.create_and_add_user('user1', 'Password1', in_memory_repo)
    auth_services.create_and_add_user('user2', 'Password1', in_memory_repo)

    user1 = auth_services.get_user('user1', in_memory_repo)
    user2 = auth_services.get_user('user2', in_memory_repo)
    track = browse_services.get_track(2, in_memory_repo)

    review1 = browse_services.create_review(track, "Great Track!", 5, user1)
    review2 = browse_services.create_review(track, "Agreed!", 4, user2)

    browse_services.add_review_to_track(track, review1, user, in_memory_repo)
    browse_services.add_review_to_track(track, review2, user, in_memory_repo)

    assert len(track.reviews) == 2

def test_can_get_reviews_for_user(in_memory_repo):
    auth_services.create_and_add_user('user1', 'Password1', in_memory_repo)
    auth_services.create_and_add_user('user2', 'Password1', in_memory_repo)

    user1 = auth_services.get_user('user1', in_memory_repo)
    track1 = browse_services.get_track(2, in_memory_repo)
    track2 = browse_services.get_track(3, in_memory_repo)

    review1 = browse_services.create_review(track1, "Great Track!", 5, user1)
    review2 = browse_services.create_review(track2, "Agreed!", 4, user1)

    browse_services.add_review_to_user(user1, review1, in_memory_repo)
    browse_services.add_review_to_user(user1, review2, in_memory_repo)

    assert len(user1.reviews) == 2

def test_can_get_no_comments_from_track(in_memory_repo):
    track = browse_services.get_track(2, in_memory_repo)
    assert len(track.reviews) == 0

def test_can_get_no_comments_from_user(in_memory_repo):
    auth_services.create_and_add_user('user', 'Password1', in_memory_repo)
    user1 = auth_services.get_user('user', in_memory_repo)
    assert len(user1.reviews) == 0