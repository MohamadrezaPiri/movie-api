import pytest
from rest_framework import status
from rest_framework.test import APIClient
from movie.models import *


@pytest.mark.django_db
class TestGetMovies:
    def test_if_returns_200(self):
        client = APIClient()
        response = client.get('/movies/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_movie_retrieved_returns_200(self):
        movie = Movie.objects.create(
            release_date='2000-02-02', imdb_votes='33333', imdb_rating='3')
        client = APIClient()
        response = client.get(f'/movies/{movie.id}/')

        assert response.status_code == status.HTTP_200_OK
