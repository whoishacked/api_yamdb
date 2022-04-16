import sys
from csv import DictReader
from os.path import exists

from django.contrib.staticfiles.finders import find
from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

DATA_MODEL = {
    'users': User,
    'category': Category,
    'titles': Title,
    'review': Review,
    'comments': Comment,
    'genre': Genre,
    'genre_title': GenreTitle,
}


class Command(BaseCommand):
    """Command for load csv data to database."""
    def handle(self, *args, **options):
        for filename, model in DATA_MODEL.items():
            if model.objects.exists():
                print(f'В базе уже есть объекты {model.__name__}!')
                result = input('Для удаления введите "Y" или что-нибудь '
                               'другое для отмены и выхода: ')
                if result == 'Y' or result == 'y':
                    model.objects.all().delete()
                    print(f'Существющие объекты {model.__name__} удалены.')
                else:
                    sys.exit(0)

            csv_file = find(f'data/{filename}.csv')

            if exists(csv_file):
                try:
                    for row in DictReader(open(csv_file, encoding='utf-8')):
                        if model == User:
                            User.objects.create(
                                id=row['id'],
                                username=row['username'],
                                email=row['email'],
                                role=row['role'],
                                bio=row['bio'],
                                first_name=row['first_name'],
                                last_name=row['last_name']
                            )
                        if model == Category:
                            Category.objects.create(
                                id=row['id'],
                                name=row['name'],
                                slug=row['slug'],
                            )
                        if model == Comment:
                            Comment.objects.create(
                                id=row['id'],
                                review=Review.objects.get(id=row['review_id']),
                                text=row['text'],
                                author=User.objects.get(id=row['author']),
                                pub_date=row['pub_date'],
                            )
                        if model == Genre:
                            Genre.objects.create(
                                id=row['id'],
                                name=row['name'],
                                slug=row['slug'],
                            )
                        if model == GenreTitle:
                            GenreTitle.objects.create(
                                id=row['id'],
                                title=Title.objects.get(id=row['title_id']),
                                genre=Genre.objects.get(id=row['genre_id']),
                            )
                        if model == Review:
                            Review.objects.create(
                                id=row['id'],
                                title=Title.objects.get(id=row['title_id']),
                                text=row['text'],
                                author=User.objects.get(id=row['author']),
                                score=row['score'],
                                pub_date=row['pub_date'],
                            )
                        if model == Title:
                            Title.objects.create(
                                id=row['id'],
                                name=row['name'],
                                year=row['year'],
                                category=Category.objects.get(
                                    id=row['category']
                                ),
                            )
                except Exception as error:
                    raise Exception(f'Ошибка добавления объекта: {error}')
            else:
                print(f'Файл {filename}.csv для заполнения '
                      f'{model.__name__} отсутвует.')

            print(f'{model.__name__}: новые объекты добавлены.')
