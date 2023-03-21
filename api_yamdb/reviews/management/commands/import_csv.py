import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

DATABASES_DICT = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Title.genre.through: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Loads the data from csv files located in static/data folder'

    def handle(self, *args, **options):
        for model, csv_file in DATABASES_DICT.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                'r',
                encoding='utf-8',
            ) as file:
                reader = csv.DictReader(file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Successfully load data'))
