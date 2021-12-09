from unittest.mock import MagicMock
import pytest

from dao.model.director import Director
from setup_db import db
from dao.director import DirectorDAO
from service.director import DirectorService




@pytest.fixture
def test_db():
    director1 = Director(id=1, name="Director_1")
    director2 = Director(id=2, name="Director_2")
    director3 = Director(id=3, name="Director_3")
    return {"1": director1, "2": director2, "3": director3}

@pytest.fixture
def director_dao():
    director_dao = DirectorDAO(db.session)
    director1 = Director(id=1, name="Director_1")
    director2 = Director(id=2, name="Director_2")
    director3 = Director(id=3, name="Director_3")
    director_dao.get_one = MagicMock(return_value=director1)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    director_dao.create = MagicMock(return_value=Director(id=4))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()
    return director_dao


class TestDirectorService():
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
            self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert isinstance(director, Director)
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        for item in directors:
            assert isinstance(item, Director)
        assert len(directors) > 0

    def test_create(self):
        director_d = {"name":"name"}
        director = self.director_service.create(director_d)
        assert isinstance(director, Director)

    def test_update(self):
        director_d = {"name": "name"}
        director = self.director_service.update(director_d)
        assert director.id != None

    def test_partially_update(self):
        director_d = {"id":1, "name": "name"}
        dao_response = self.director_service.partially_update(director_d)
        assert dao_response == None

    def test_delete(self):
        dao_response = self.director_service.delete(5)
        assert dao_response == None
