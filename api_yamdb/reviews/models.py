#  from django.contrib.auth import get_user_model
from django.db import models

#  User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    """Review model."""
    # author = models.ForeignKey(
    #    User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    """Commentary model."""
    # author = models.ForeignKey(
    #    User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
