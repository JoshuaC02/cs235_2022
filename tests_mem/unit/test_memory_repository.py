import pytest

from music.domainmodel import album, artist, genre, review, track, user
from music.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):  # Passes
    # Simulated new user added to repository
    new_user = user.User(1, "Jeff", "Password1")
    in_memory_repo.add_user(new_user)

    # Check User has been added to repository
    assert in_memory_repo.get_user("Jeff") is new_user


def test_repository_can_not_add_invalid_user(in_memory_repo):  # Passes
    """# Simulated invalid User
    new_user = user.User(-1, "Jeff", "Password1")

    # Check that invalid user raises error
    with pytest.raises(RepositoryException):
        in_memory_repo.add_user(new_user)"""

    # Check that invalid user raises error
    with pytest.raises(ValueError):
        # Simulated invalid User
        new_user = user.User(-1, "Jeff", "Password1")
        in_memory_repo.add_user(new_user)


def test_repository_can_not_add_invalid_user_object(in_memory_repo):  # Passes
    # Simulated invalid user object
    new_user = "user"

    # Check RepositoryException is raised
    with pytest.raises(RepositoryException):
        in_memory_repo.add_user(new_user)


def test_repository_can_retrieve_a_user(in_memory_repo):  # Passes
    # Simulated user added to repository
    new_user = user.User(1, "Jeff", "Password1")
    in_memory_repo.add_user(new_user)
    # Retrieve simulated user
    retrieve_user = in_memory_repo.get_user("Jeff")

    # Check a retrieved user matches simulated user
    assert retrieve_user == new_user


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):  # Passes
    # Retrieve user that does not exist
    retrieve_user = in_memory_repo.get_user("MrDoesNotExist")

    # Check program returns None when user does not exist
    assert retrieve_user is None


def test_repository_can_add_review_to_user(in_memory_repo):  # Passes
    # Simulated user, track, and review
    new_user = user.User(1, "Jeff", "Password1")
    in_memory_repo.add_user(new_user)
    new_track = track.Track(0, "Track title")
    in_memory_repo.add_track(new_track)
    new_review = review.Review(new_track, "review", 5, new_user)
    in_memory_repo.add_review_to_user(new_user, new_review)

    # Check review is successfully added to the user
    assert new_user.reviews == [new_review]


def test_repository_can_overwrite_user_review(in_memory_repo):  # Passes
    # Simulated user, track, and review
    new_user = user.User(1, "Jeff", "Password1")
    in_memory_repo.add_user(new_user)
    new_track = track.Track(0, "Track title")
    in_memory_repo.add_track(new_track)
    new_review = review.Review(new_track, "review", 5, new_user)
    in_memory_repo.add_review_to_user(new_user, new_review)

    # Check review is successfully added to the user
    assert new_user.reviews == [new_review]
    # Change review for same track and user
    new_review = review.Review(new_track, "review2", 1, new_user)
    in_memory_repo.add_review_to_user(new_user, new_review)
    # Check review has updated rather than adding new review for same track and user
    assert new_user.reviews == [new_review]


def test_repository_can_add_review_to_track(in_memory_repo):  # Passes
    # Simulated user, track, and review
    new_user = user.User(1, "Jeff", "Password1")
    in_memory_repo.add_user(new_user)
    new_track = track.Track(0, "Track title")
    in_memory_repo.add_track(new_track)
    new_review = review.Review(new_track, "review", 5, new_user)
    in_memory_repo.add_review_to_track(new_track, new_review, new_user)

    # Check review is successfully added to track object
    assert new_track.reviews == [new_review]


def test_repository_can_overwrite_track_review(in_memory_repo):  # Passes
    # Simulated user, track, and review
    new_user = user.User(1, "Jeff", "Password1")
    in_memory_repo.add_user(new_user)
    new_track = track.Track(0, "Track title")
    in_memory_repo.add_track(new_track)
    new_review = review.Review(new_track, "review", 5, new_user)
    in_memory_repo.add_review_to_track(new_track, new_review, new_user)

    # Check review is successfully added to track object
    assert new_track.reviews == [new_review]
    # Change review for same track and user
    new_review = review.Review(new_track, "review2", 1, new_user)
    in_memory_repo.add_review_to_track(new_track, new_review, new_user)
    # Check review has updated rather than adding new review for same track and user
    assert new_track.reviews == [new_review]


def test_repository_can_add_a_track(in_memory_repo):  # Passes
    # Number of tracks before adding a new track
    tracks_before_add = in_memory_repo.get_number_of_tracks()
    # Simulated track added to repository
    new_track = track.Track(0, "Track title")
    in_memory_repo.add_track(new_track)

    # Check count is now one greater indicated track has been added to repository
    assert in_memory_repo.get_number_of_tracks() == tracks_before_add + 1


def test_repository_can_not_add_invalid_track(in_memory_repo):  # Passes
    """# Simulated invalid track
    new_track = track.Track(-1, "Track Name")

    # Check that invalid track raises error
    with pytest.raises(RepositoryException):
        in_memory_repo.add_track(new_track)"""

    # Check that invalid track raises error
    with pytest.raises(ValueError):
        # Simulated invalid track
        new_track = track.Track(-1, "Track Name")
        in_memory_repo.add_track(new_track)


def test_repository_can_not_add_invalid_track_object(in_memory_repo):  # Passes
    # Simulated invalid track object
    new_track = "track"

    # Check RepositoryException is raised
    with pytest.raises(RepositoryException):
        in_memory_repo.add_track(new_track)


def test_repository_can_add_track_to_sort(in_memory_repo):  # Passes
    # Simulated track added to repository
    new_track = track.Track(0, "Track title")
    in_memory_repo.add_track_to_sort(new_track)
    # Retrieve list of sorted tracks
    sorted_list = in_memory_repo.get_sorted_tracks()

    # Check the last added track is the simulated track
    assert sorted_list[-1] is new_track


def test_repository_can_not_add_invalid_track_to_sort(in_memory_repo):  # Passes
    """# Simulated invalid track
    new_track = track.Track(-1, "Track Name")

    # Check that invalid track raises error
    with pytest.raises(RepositoryException):
        in_memory_repo.add_track_to_sort(new_track)"""


    # Check that invalid track raises error
    with pytest.raises(ValueError):
        # Simulated invalid track
        new_track = track.Track(-1, "Track Name")
        in_memory_repo.add_track_to_sort(new_track)


def test_repository_can_get_track_from_id(in_memory_repo):  # Passes
    # Simulated track added to repository
    new_track = track.Track(0, "Track title")
    in_memory_repo.add_track(new_track)
    # Get track with track id 0 (Simulated track)
    track_found = in_memory_repo.get_track(0)

    # Check found track matches simulated track
    assert track_found is new_track


def test_repository_does_not_return_invalid_track_from_id(in_memory_repo):  # Passes
    # Get track with track id 0 (Has not been added)
    track_found = in_memory_repo.get_track(0)

    # Check program returns None when track does not exist
    assert track_found is None


def test_repository_gets_number_of_tracks(in_memory_repo):  # Passes
    # Number of tracks from given CSV is 2000
    number_of_initial_tracks = 2000

    # Check that function correctly returns number of tracks in repository
    assert in_memory_repo.get_number_of_tracks() == number_of_initial_tracks


def test_repository_gets_specified_list_of_tracks(in_memory_repo):  # Passes
    # Simulated search for Page 2 consisting of 30 songs per page (e.g. second 30 songs)
    starting_page = 2
    songs_per_page = 30
    specified_tracks = in_memory_repo.get_list_of_tracks(starting_page, songs_per_page)

    # Check tracks match ones from sorted tracks list
    assert specified_tracks == in_memory_repo.get_sorted_tracks()[30:60]


def test_repository_can_add_album(in_memory_repo):  # Passes
    # Simulated album added to repository
    new_album = album.Album(0, "Album Title")
    in_memory_repo.add_album(new_album)
    # Find last added album
    last_added_album = in_memory_repo.get_albums()[-1]

    # Check the last added album is the newly created album
    assert last_added_album is new_album


def test_repository_can_not_add_invalid_album(in_memory_repo):  # Passes
    """# Simulated invalid album
    new_album = album.Album(-1, "Album Name")

    # Check that invalid album raises error
    with pytest.raises(RepositoryException):
        in_memory_repo.add_album(new_album)"""


    # Check that invalid album raises error
    with pytest.raises(ValueError):
        # Simulated invalid album
        new_album = album.Album(-1, "Album Name")
        in_memory_repo.add_album(new_album)


def test_repository_can_not_add_invalid_album_object(in_memory_repo):  # Passes
    # Simulated invalid album object
    new_album = "album"

    # Check RepositoryException is raised
    with pytest.raises(RepositoryException):
        in_memory_repo.add_album(new_album)


def test_repository_can_get_albums(in_memory_repo):  # Passes
    # Run get_albums function
    albums_from_function = in_memory_repo.get_albums()

    # Check function returns a list of Albums
    assert all(isinstance(x, album.Album) for x in albums_from_function)


def test_repository_can_add_artist(in_memory_repo):  # Passes
    # Simulated artist added to repository
    new_artist = artist.Artist(0, "Artist Name")
    in_memory_repo.add_artist(new_artist)
    # Find last added artist
    last_added_artist = in_memory_repo.get_artists()[-1]

    # Check last added album is the newly created artist
    assert last_added_artist is new_artist


def test_repository_can_not_add_invalid_artist(in_memory_repo):  # Passes
    """
    # Simulated invalid artist
    new_artist = artist.Artist("one", "Artist Name")

    # Check that invalid artist raises error
    with pytest.raises(RepositoryException):
        in_memory_repo.add_artist(new_artist)
    """
    # Check that invalid artist raises error
    with pytest.raises(ValueError):
        # Simulated invalid artist
        new_artist = artist.Artist("one", "Artist Name")
        in_memory_repo.add_artist(new_artist)


def test_repository_can_not_add_invalid_artist_object(in_memory_repo):  # Passes
    # Simulated invalid artist object
    new_artist = "track"

    # Check RepositoryException is raised
    with pytest.raises(RepositoryException):
        in_memory_repo.add_artist(new_artist)


def test_repository_can_get_artists(in_memory_repo):  # Passes
    # Run get_artists function
    artists_from_function = in_memory_repo.get_artists()

    # Check functions returns a list of Artists
    assert all(isinstance(x, artist.Artist) for x in artists_from_function)


def test_repository_can_add_genre(in_memory_repo):  # Passes
    # Simulated genre added to repository
    new_genre = genre.Genre(0, "Genre Name")
    in_memory_repo.add_genre(new_genre)
    # Find last added genre
    last_added_genre = in_memory_repo.get_genres()[-1]

    # Check last added genre is the newly created genre
    assert last_added_genre is new_genre


def test_repository_can_not_add_invalid_genre(in_memory_repo):  # Passes
   """ # Simulated invalid genre
    new_genre = genre.Genre(-1, "Genre Name")

    # Check that invalid genre raises error
    with pytest.raises(RepositoryException):
        in_memory_repo.add_genre(new_genre)"""


   # Check that invalid genre raises error
   with pytest.raises(ValueError):
       # Simulated invalid genre
       new_genre = genre.Genre(-1, "Genre Name")
       in_memory_repo.add_genre(new_genre)


def test_repository_can_not_add_invalid_genre_object(in_memory_repo):  # Passes
    # Simulated invalid genre object
    new_genre = "genre"

    # Check RepositoryException is raised
    with pytest.raises(RepositoryException):
        in_memory_repo.add_genre(new_genre)


def test_repository_can_get_genres(in_memory_repo):  # Passes
    # Run get_genres function
    genres_from_function = in_memory_repo.get_genres()

    # Check functions returns a list of Genres
    assert all(isinstance(x, genre.Genre) for x in genres_from_function)


def test_repository_can_add_track_dictionary(in_memory_repo):  # Passes
    # Simulated dictionary object
    new_track = track.Track(0, "Track Name")
    new_album = album.Album(0, "Album Title")
    new_artist = artist.Artist(0, "Artist Name")
    in_memory_repo.add_track_dict(new_track, new_album, new_artist)
    track_dict = in_memory_repo.get_track_dict()
    # Correct format that the function should create with values
    track_dict_format = {new_track: [new_track.title, new_album.title, new_artist.full_name]}

    # Check the last added object matches the format with correct values
    assert list(track_dict.items())[-1] == list(track_dict_format.items())[-1]


def test_repository_can_get_track_dict(in_memory_repo):  # Passes
    # Run function to get track dictionary
    track_dicts_from_function = in_memory_repo.get_track_dict()

    # Check that the return is of type dict
    assert type(track_dicts_from_function) == dict


def test_repository_can_get_tracks_from_track_dict_with_any_value(in_memory_repo):  # Passes
    # Simulated track_dict
    new_track = track.Track(0, "Track Name")
    new_album = album.Album(0, "Album Title")
    new_artist = artist.Artist(0, "Artist Name")
    in_memory_repo.add_track_dict(new_track, new_album, new_artist)
    # Return when searching via track title
    return1 = in_memory_repo.return_track_from_dict(new_track.title)
    # Return when searching via album title
    return2 = in_memory_repo.return_track_from_dict(new_album.title)
    # Return when searching via artist name
    return3 = in_memory_repo.return_track_from_dict(new_artist.full_name)

    # Check all "returns" return the relative track object
    # This means the function works and can search for a track object by all these values
    assert return1 == return2 == return3 == [new_track]


def test_repository_can_sort_tracks_by_track_name(in_memory_repo):  # Passes
    # Simulated track
    new_track = track.Track(512, '"')
    in_memory_repo.add_track(new_track)
    # Sort tracks by track name ascending
    in_memory_repo.sort_tracks("get_track_name", False)

    # Check tracks are sorted - our created track should be first
    # Also confirms that searching in ascending order works
    assert in_memory_repo.get_sorted_tracks()[0] is new_track


def test_repository_can_sort_tracks_by_track_id(in_memory_repo):  # Passes
    # Simulated track
    new_track = track.Track(0, "First Track After Sort")
    in_memory_repo.add_track(new_track)
    # Sort tracks by track id ascending
    in_memory_repo.sort_tracks("get_track_id", False)

    # Check tracks are sorted - our created track should be first
    assert in_memory_repo.get_sorted_tracks()[0] is new_track


def test_repository_can_sort_tracks_by_track_duration(in_memory_repo):  # Passes
    # Simulated track
    new_track = track.Track(0, "First Track After Sort")
    new_track.track_duration = 1
    in_memory_repo.add_track(new_track)
    # Sort tracks by duration ascending
    in_memory_repo.sort_tracks("get_track_duration", False)

    # Check tracks are sorted - our created track should be first
    assert in_memory_repo.get_sorted_tracks()[0] is new_track


def test_repository_can_sort_tracks_by_artist_name(in_memory_repo):  # Passes
    # Simulated track and artist
    new_track = track.Track(0, "First Track After Sort")
    new_artist = artist.Artist(0, "'")
    new_track.artist = new_artist
    in_memory_repo.add_track(new_track)
    # Sort tracks by duration ascending
    in_memory_repo.sort_tracks("get_track_artist_name", False)

    # Check tracks are sorted - our created track should be first
    assert in_memory_repo.get_sorted_tracks()[0] is new_track


def test_repository_can_sort_tracks_by_album_name(in_memory_repo):  # Passes
    # Simulated track and album
    new_track = track.Track(0, "First Track After Sort")
    new_album = album.Album(0, '"AAA"')
    new_track.album = new_album
    in_memory_repo.add_track(new_track)
    # Sort tracks by duration ascending
    in_memory_repo.sort_tracks("get_track_album_name", False)

    # Check tracks are sorted - our created track should be first
    assert in_memory_repo.get_sorted_tracks()[0] is new_track


def test_repository_can_sort_tracks_by_rating(in_memory_repo):  # Passes
    # Simulated track and album
    new_track = track.Track(0, "First Track After Sort")
    new_user = user.User(0, "USERNAME", "Password1")
    new_review = review.Review(new_track, "review", 5, new_user)
    new_track.add_review(new_review)
    in_memory_repo.add_track(new_track)
    # Sort tracks by duration descending (The highest review first)
    in_memory_repo.sort_tracks("get_track_rating", True)

    # Check tracks are sorted - our created track should be first
    # Also confirms that searching in descending order works
    assert in_memory_repo.get_sorted_tracks()[0] is new_track


def test_repository_can_get_track_name(in_memory_repo):  # Passes
    # Simulated track
    new_track = track.Track(0, "Track Name")

    # Check function returns track name from new track
    assert in_memory_repo.get_track_name(new_track) is "Track Name"


def test_repository_can_get_track_id(in_memory_repo):  # Passes
    # Simulated track
    new_track = track.Track(0, "Track Name")

    # Check function returns track id from new track
    assert in_memory_repo.get_track_id(new_track) is 0


def test_repository_can_get_track_duration(in_memory_repo):  # Passes
    # Simulated track with track duration
    new_track = track.Track(0, "Track Name")
    new_track.track_duration = 10

    # Check function returns track duration from new track
    assert in_memory_repo.get_track_duration(new_track) is 10


def test_repository_can_get_track_artist_name(in_memory_repo):  # Passes
    # Simulated track with artist
    new_track = track.Track(0, "Track Name")
    new_artist = artist.Artist(0, "Artist Name")
    new_track.artist = new_artist

    # Check function returns artist name from new track
    assert in_memory_repo.get_track_artist_name(new_track) is "Artist Name"


def test_repository_can_get_track_album_name(in_memory_repo):  # Passes
    # Simulated track with album
    new_track = track.Track(0, "Track Name")
    new_album = album.Album(0, "Album Name")
    new_track.album = new_album

    # Check function returns album name from new track
    assert in_memory_repo.get_track_album_name(new_track) is "Album Name"


def test_repository_can_get_track_rating(in_memory_repo):  # Passes
    # Simulated track with review
    new_track = track.Track(0, "Track Name")
    new_user = user.User(0, "USERNAME", "Password1")
    new_review = review.Review(new_track, "review", 5, new_user)
    new_track.add_review(new_review)

    # Check function returns review track rating from new track
    assert in_memory_repo.get_track_rating(new_track) == 5.0


def test_repository_recommends_tracks_correctly(in_memory_repo):  # Passes
    # Get track from CSV that already has genres, album, artist, duration
    new_track = in_memory_repo.get_track(2)
    # Simulate user and 5-star review
    new_user = user.User(0, "USERNAME", "Password1")
    new_review = review.Review(new_track, "review", 5, new_user)
    new_user.add_review(new_review)
    # Recommend tracks based on high reviews
    tracks_recommended = in_memory_repo.recommend_tracks(new_user)

    # Flag created for assert check
    genre_match = False
    # Loop through each track in recommended tracks
    for track_object in tracks_recommended:
        # Loop through each genre in recommended track
        for object_genre in track_object.genres:
            # Loop through each genre in 5-star reviewed track
            for track_genre in new_track.genres:
                # Check if tracks share a genre
                if object_genre == track_genre:
                    genre_match = True
        # Check if tracks share an artist, album, or genre; or have a similar duration length
        # (These are the criteria for recommending a track)
        if track_object.artist != new_track.artist and track_object.album != new_track.album and not genre_match and not(track_object.track_duration-15 <= new_track.track_duration <= track_object.track_duration+15):
            # Function does not work correctly if criteria is NOT met
            assert False
    # Else, criteria is met
    # Check that the function meets prior criteria and returns a list of recommended tracks
        # This confirms that the function works correctly
        # This also confirms that the followings functions work correctly:
            # "recommend_from_artist, "recommend_from_genre", "recommend_from_album", "recommend_from_duration"
    assert tracks_recommended is not [] and all(isinstance(x, track.Track) for x in tracks_recommended)


def test_repository_does_not_recommend_tracks_from_low_rated_reviews(in_memory_repo):  # Passes
    # Get track from CSV that already has genres, album, artist, duration
    new_track = in_memory_repo.get_track(2)
    # Simulate user and 1-star review
    new_user = user.User(0, "USERNAME", "Password1")
    new_review = review.Review(new_track, "review", 1, new_user)
    new_user.add_review(new_review)
    # Recommend tracks based on high reviews
    tracks_recommended = in_memory_repo.recommend_tracks(new_user)

    # Check that the function returns an empty list as nothing is recommended
    assert tracks_recommended == []


def test_repository_does_not_recommend_same_track(in_memory_repo):  # Passes
    # Get track from CSV that already has genres, album, artist, duration
    new_track = in_memory_repo.get_track(2)
    # Simulate user and 1-star review
    new_user = user.User(0, "USERNAME", "Password1")
    new_review = review.Review(new_track, "review", 5, new_user)
    new_user.add_review(new_review)
    # Recommend tracks based on high reviews
    tracks_recommended = in_memory_repo.recommend_tracks(new_user)

    # Check that the function does NOT recommend the initial track that has been reviewed
    assert new_track not in tracks_recommended


def test_repository_can_generate_unique_user_id(in_memory_repo):  # Passes
    # Run function to generate new ID
    new_id = in_memory_repo.generate_user_id()
    # Store current user IDs
    current_user_ids = []
    for user_object in in_memory_repo.get_users():
        current_user_ids.append(user_object.user.user_id)

    # Check the newly generated ID is unique
    assert new_id not in current_user_ids

