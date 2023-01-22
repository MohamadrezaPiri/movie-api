from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    cast = models.TextField()
    crew = models.TextField()
    plot = models.TextField()
    poster = models.URLField()
    imdb_rating = models.FloatField()
    imdb_votes = models.TextField()
    imdb_id = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
