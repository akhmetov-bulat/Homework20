from unittest.mock import MagicMock
import pytest

from dao.model.genre import Genre
from setup_db import db
from dao.genre import GenreDAO
from service.genre import GenreService




@pytest.fixture
def test_db():
    genre1 = Genre(id=1, name="Genre_1")
    genre2 = Genre(id=2, name="Genre_2")
    genre3 = Genre(id=3, name="Genre_3")
    return {"1": genre1, "2": genre2, "3": genre3}

@pytest.fixture
def genre_dao():
    genre_dao = GenreDAO(db.session)
    genre1 = Genre(id=1, name="Genre_1")
    genre2 = Genre(id=2, name="Genre_2")
    genre3 = Genre(id=3, name="Genre_3")
    genre_dao.get_one = MagicMock(return_value=genre1)
    genre_dao.get_all = MagicMock(return_value=[genre1, genre2, genre3])
    genre_dao.create = MagicMock(return_value=Genre(id=4))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()
    return genre_dao


class TestGenreService():
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
            self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre != None
        assert genre.id != None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres)>0

    def test_create(self):
        genre_d = {"name":"name"}
        genre = self.genre_service.create(genre_d)
        assert genre.id != None

    def test_update(self):
        genre_d = {"name": "name"}
        genre = self.genre_service.update(genre_d)
        assert genre.id != None

    def test_partially_update(self):
        genre_d = {"id":1, "name": "name"}
        dao_response = self.genre_service.partially_update(genre_d)
        assert dao_response == None

    def test_delete(self):
        dao_response = self.genre_service.delete(5)
        assert dao_response == None
