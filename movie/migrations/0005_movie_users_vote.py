# Generated by Django 4.1.5 on 2023-01-23 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='users_vote',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=1),
            preserve_default=False,
        ),
    ]