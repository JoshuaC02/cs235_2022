"""Initialize Flask app."""

from flask import Flask, render_template, redirect, url_for, session, request, Blueprint, abort
from flask import current_app as app

from pathlib import Path

# imports from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate
from music.adapters.database_repository import SqlAlchemyRepository
from music.adapters.repository_populate import populate as db_populate
from music.adapters.orm import metadata, map_model_to_tables
def create_app(test_config=None):
    print("CREATE APP RUN")
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    
    if app.config['REPOSITORY'] == 'memory':
        repo.track_repo = MemoryRepository()
        populate(data_path, repo.track_repo)
        
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=database_echo)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.track_repo = SqlAlchemyRepository(session_factory)
        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print('REPOPULATING DATABASE...')
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())
            
            map_model_to_tables()
            database_mode = True
            db_populate(data_path, repo.track_repo, database_mode)
        
        else:
            map_model_to_tables()

    #add the ability to access the repo from current_app
    app.repo = repo.track_repo
    #app.repo.update_tracks()
    app.repo.sort_tracks("get_track_id", False)
    @app.route('/')
    def home():
        username = None
        if 'username' in session:
            if browse.services.get_user(session['username'], app.repo) == None:
                username = None
            else:
                username = session['username']
        return render_template('index.html', username=username)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
        
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.track_repo, SqlAlchemyRepository):
                repo.track_repo.reset_session()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.track_repo, SqlAlchemyRepository):
                repo.track_repo.close_session()

    return app



