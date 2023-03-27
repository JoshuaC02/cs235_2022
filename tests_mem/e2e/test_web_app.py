import pytest

from music.authentication import services as auth_services
"""
from ...music.browse import services as browse_services
"""
from flask import session

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters long, contain an upper case letter, a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'That username is already taken!'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    client.post(
        '/authentication/register',
        data={'username': 'fmercury', 'password': 'Password1'}
    )
    response = client.post(
        '/authentication/register',
        data={'username': user_name, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    # Create user
    auth.register()

    # Test login page retrival
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Login
    response = auth.login()

    assert response.headers['Location'] == '/'

    with client:
        client.get('/')
        assert session['username'] == 'fmercury'

def test_logout(client, auth):
    # First, sign in to have a user to sign out
    auth.register()
    auth.login()

    with client:
        client.get('/')
        assert session['username'] == 'fmercury'

    with client:
        # With a user confirmed signed in, now attempt to signout
        auth.logout()
        assert 'username' not in session

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home - MusicWiki' in response.data

def test_login_required_to_review(client):
    response = client.post('/tracks/review/2')
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

def test_login_required_to_recommend(client):
    response = client.get('/tracks/recommendations')
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

def test_review(client, auth):
    # Login a user.
    auth.register()
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/tracks/review/2')

    response = client.post(
        '/tracks/review/2',
        data={'review_comment': 'Awesome track!', 'out_of_5': 3}
    )
    assert response.headers['Location'] == '/tracks/browse'

@pytest.mark.parametrize(('comment', 'out_of_5', 'messages'), (
        ('abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 5, (b'Maximum of 250 characters')),
))
def test_comment_with_invalid_input(client, auth, comment, out_of_5, messages):
    # Login a user.
    auth.register()
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/tracks/review/2',
        data={'review_comment': comment, 'out_of_5': out_of_5}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data