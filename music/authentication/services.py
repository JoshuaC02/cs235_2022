from flask import session
from music.domainmodel.user import User
from music.adapters.repository import AbstractRepository
from werkzeug.security import generate_password_hash, check_password_hash

class UsernameInUse(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass

def sign_in(current_session: session, username, password, repo):
    user = get_user(username, repo)
    if user == None:
        raise UnknownUserException()

    if not authenticate_user(username, password, repo):
        raise AuthenticationException()

    current_session.clear()
    current_session['username'] = username

def sign_out(current_session: session):
    current_session.clear()

def create_and_add_user(username, password, repo):
    check_user = get_user(username, repo)
    if check_user != None:
        raise UsernameInUse()
    
    password_hash = generate_password_hash(password)

    user = User(repo.generate_user_id(), username, password_hash)

    repo.add_user(user)

def authenticate_user(passed_username, passed_password, repo):
    user = repo.get_user(passed_username)
    return check_password_hash(user.password, passed_password)

def get_user(username, repo):
    return repo.get_user(username)


