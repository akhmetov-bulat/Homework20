from unittest.mock import MagicMock
import pytest

from dao.model.movie import Movie
from setup_db import db
from dao.movie import MovieDAO
from service.movie import MovieService




@pytest.fixture
def test_db(*args, **kwargs):
    film1 = Movie(id=1, title="Film_1",
                  description="Lorem ipsum dolor",
                  trailer="http://youtube.com", year=2021,
                  rating=9.9, genre_id=1, director_id=1)
    film2 = Movie(id=2, title="Film_2",
                  description="Lorem ipsum dolor",
                  trailer="http://youtube.com", year=2021,
                  rating=9.9, genre_id=1, director_id=1)
    film3 = Movie(id=3, title="Film_3",
                  description="Lorem ipsum dolor",
                  trailer="http://youtube.com", year=2021,
                  rating=9.9, genre_id=1, director_id=1)
    if kwargs["id"]:
        return film3
    return {"1": film1, "2": film2, "3": film3}

@pytest.fixture
def movie_dao():
    movie_dao = MovieDAO(db.session)
    film1 = Movie(id=1, title="Film_1",
                  description="Lorem ipsum dolor",
                  trailer="http://youtube.com", year=2021,
                  rating=9.9, genre_id=1, director_id=1)
    film2 = Movie(id=2, title="Film_2",
                  description="Lorem ipsum dolor",
                  trailer="http://youtube.com", year=2021,
                  rating=9.9, genre_id=1, director_id=1)
    film3 = Movie(id=3, title="Film_3",
                  description="Lorem ipsum dolor",
                  trailer="http://youtube.com", year=2021,
                  rating=9.9, genre_id=1, director_id=1)
    movie_dao.get_one = MagicMock(return_value=film3)
    movie_dao.get_all = MagicMock(return_value=[film1, film2, film3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService():
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
            self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(3)
        assert isinstance(movie, Movie)
        assert movie.id == 3

    def test_get_all(self):
        movies = self.movie_service.get_all()
        for item in movies:
            assert isinstance(item, Movie)
        assert len(movies)>0

    def test_create(self):
        movie_d = {"name":"name"}
        movie = self.movie_service.create(movie_d)
        assert isinstance(movie, Movie)

    def test_update(self):
        movie_d = {"name": "name"}
        movie = self.movie_service.update(movie_d)
        assert movie.id != None

    def test_partially_update(self):
        movie_d = {"id":1, "name": "name"}
        dao_response = self.movie_service.partially_update(movie_d)
        assert dao_response == None

    def test_delete(self):
        dao_response = self.movie_service.delete(5)
        assert dao_response == None
