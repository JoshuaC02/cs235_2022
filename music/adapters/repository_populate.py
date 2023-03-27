from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters import csv_data_importer
from music.adapters import database_repository


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    #csv_data_importer.load_all(data_path, repo)
    
    csv_data_importer.load_artists(data_path, repo)
    csv_data_importer.load_albums(data_path, repo)
    csv_data_importer.load_tracks_and_genres(data_path, repo)
    
    
    #database_repository.SqlAlchemyRepository(AbstractRepository).update_tracks()
    #csv_data_importer.load_tracks(data_path, repo)
    #csv_data_importer.load_genres(data_path, repo, database_mode)