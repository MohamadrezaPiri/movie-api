# Generated by Django 4.1.5 on 2023-01-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.DateTimeField()),
                ('cast', models.TextField()),
                ('crew', models.TextField()),
                ('plot', models.TextField()),
                ('poster', models.URLField()),
                ('imdb_rating', models.FloatField()),
                ('imdb_votes', models.IntegerField()),
                ('imdb_id', models.CharField(max_length=10)),
            ],
        ),
    ]