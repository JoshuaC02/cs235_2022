from pickle import FALSE
from typing import Counter
from sqlalchemy import Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relationship, synonym
from music.domainmodel import album, artist, genre, playlist, review, track, user

metadata = MetaData()

user_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
    # TODO: add relationship between reviews. liked tracks and playlist can be ignored, not implemented features
)
album_table = Table(
    'albums', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('album_url', String(1024)),
    Column('album_type', String(255)),
    Column('release_year', Integer)
)
artist_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True),
    Column('full_name', String(255), nullable=False)
)
genre_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, unique=False),
    Column('genre_name', String(255), nullable=False)
)
review_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('track_id', ForeignKey('tracks.id')),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=FALSE)
)
track_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('title', String(255), nullable=False),
    Column('album_id', ForeignKey('albums.id')),
    Column('artist_id', ForeignKey('artists.id')),
    Column('duration', Integer, nullable=False),
    Column('track_url', String(1024)), 
)
track_genre_table = Table(
    'track_genre', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('genre_id', ForeignKey('genres.id')),
)
sorted_track_table = Table(
    'sort_track', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', Integer, nullable=False)
)

def map_model_to_tables():
    mapper(user.User, user_table, properties={
        '_User__user_id': user_table.c.id,
        '_User__user_name': user_table.c.user_name,
        '_User__password': user_table.c.password,
        '_User__reviews' : relationship(review.Review, backref='_Review__user')
    })
    mapper(album.Album, album_table, properties={
        '_Album__album_id': album_table.c.id,
        '_Album__title': album_table.c.title,
        '_Album__album_url': album_table.c.album_url,
        '_Album__album_type': album_table.c.album_type,
        '_Album__release_year': album_table.c.release_year,
        '_Album__tracks': relationship(track.Track, backref='_Track__album')
    })

    mapper(artist.Artist, artist_table, properties={
        '_Artist__artist_id': artist_table.c.id,
        '_Artist__full_name': artist_table.c.full_name,
        '_Artist__tracks': relationship(track.Track, backref='_Track__artist')
    })
    mapper(genre.Genre, genre_table, properties={
        '_Genre__genre_id': genre_table.c.id,
        '_Genre__name': genre_table.c.genre_name,
        '_Genre__applied_to': relationship(track.Track, secondary=track_genre_table, back_populates='_Track__genres')
    })
    mapper(review.Review, review_table, properties={
        '_Review__review_text': review_table.c.review,
        '_Review__rating': review_table.c.rating,
        '_Review__timestamp': review_table.c.timestamp
    })
    mapper(track.Track, track_table, properties={
        '_Track__track_id': track_table.c.id,
        '_Track__title': track_table.c.title,
        #'_Track__artist_id': relationship(artist.Artist),
        '_Track__track_duration': track_table.c.duration,
        '_Track__track_url': track_table.c.track_url,
        '_Track__genres': relationship(genre.Genre, secondary=track_genre_table, back_populates='_Genre__applied_to'),
        '_Track__reviews': relationship(review.Review, backref='_Review__track'),
        #'_Track__album': relationship(album.Album),#, backref='_Album__tracks'), # TODO: NOT COMPLETE/WORKING
        #'_Track__artist': relationship(artist.Artist)#, backref='_Artist__tracks') # TODO: NOT COMPLETE/WORKING
    })
