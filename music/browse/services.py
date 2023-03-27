from flask import session

from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

def sort_tracks(input: str, sort_order: bool, repo):
    repo.sort_tracks(input, sort_order)

def change_sort_method(data, repo):
    if data != "":
        if data == "get_track_rating":
            repo.sort_tracks(data, True)
        else:
            repo.sort_tracks(data, False)

def get_list_of_tracks(page, per_page, repo):
    return repo.get_list_of_tracks(page, per_page)

def get_track(variable, repo):
    return repo.get_track(variable)

def return_track_from_dict(data, repo):
    return repo.return_track_from_dict(data)

def get_user(username, repo):
    return repo.get_user(username)

def create_review(current_track: Track, comment: str, rating: int, current_user: User):
    return Review(current_track, comment, rating, current_user)

def add_review_to_user(current_user: User, new_review: Review, repo):
    repo.add_review_to_user(current_user, new_review)

def add_review_to_track(current_track: Track, new_review: Review, current_user: User, repo):
    repo.add_review_to_track(current_track, new_review, current_user)
    
    
def recommend_track(username, repo):
    return repo.recommend_tracks(repo.get_user(username))

def get_number_of_tracks(repo):
    return repo.get_number_of_tracks()