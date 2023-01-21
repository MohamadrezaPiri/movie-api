from django.db import models

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
