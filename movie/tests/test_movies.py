import pytest
from rest_framework import status
from model_bakery import baker
from movie.models import *


@pytest.mark.django_db
class TestGetMovies:
    def test_if_returns_200(self, api_client):
        response = api_client.get('/movies/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_movie_retrieved_returns_200(self, api_client):
        movie = baker.make(Movie)

        response = api_client.get(f'/movies/{movie.id}/')

        assert response.status_code == status.HTTP_200_OK
