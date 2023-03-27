import pytest
from music import create_app
from music.adapters import memory_repository
from music.adapters.memory_repository import MemoryRepository

from utils import get_project_root

# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests_mem" / "data"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, username='fmercury', password='Password1'):
        return self.__client.post(
            '/authentication/register',
            data={'username': 'fmercury', 'password': 'Password1'}
        )   

    def login(self, username='fmercury', password='Password1'):
        return self.__client.post(
            '/authentication/login',
            data={'username': 'fmercury', 'password': 'Password1'}
        )   

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)