# Generated by Django 4.1.5 on 2023-01-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_movie_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_votes',
            field=models.TextField(),
        ),
    ]