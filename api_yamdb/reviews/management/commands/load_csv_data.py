from csv import DictReader
from os.path import exists
from django.core.management import BaseCommand
from django.contrib.staticfiles.finders import find
from reviews.models import (Title, Category, Comment, Genre, GenreTitle, User,
                            Review)

DATA_MODEL = {
    'users': User,
    'category': Category,
    'titles': Title,
    'genre': Genre,
    'genre_title': GenreTitle,
    'review': Review,
    'comments': Comment,
}


class Command(BaseCommand):

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
                    return

            csv_file = find(f'data/{filename}.csv')

            if exists(csv_file):
                for row in DictReader(open(csv_file)):
                    if model == User:
                        new_item = User(
                            id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name']
                        )
                    if model == Category:
                        new_item = Category(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                    if model == Comment:
                        new_item = Comment(
                            id=row['id'],
                            review_id=Review.objects.get(id=row['review_id']),
                            text=row['text'],
                            author=User.objects.get(id=row['author']),
                            pub_date=row['pub_date'],
                        )
                    if model == Genre:
                        new_item = Genre(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                    if model == GenreTitle:
                        new_item = GenreTitle(
                            id=row['id'],
                            title_id=Title.objects.get(id=row['title_id']),
                            genre_id=Genre.objects.get(id=row['genre_id']),
                        )
                    if model == Review:
                        new_item = Review(
                            id=row['id'],
                            title_id=Title.objects.get(id=row['title_id']),
                            text=row['text'],
                            author=User.objects.get(id=row['author']),
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                    if model == Title:
                        new_item = Title(
                            id=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category=Category.objects.get(
                                id=row['category']
                            ),
                        )
                    new_item.save()
            else:
                print(f'Файл {filename}.csv для заполнения '
                      f'{model.__name__} не найден.')

            print(f'{model.__name__}: новые объекты добавлены.')
