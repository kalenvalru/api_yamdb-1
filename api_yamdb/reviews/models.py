from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, SET_NULL, CharField, DateTimeField,
                              ForeignKey, IntegerField, ManyToManyField, Model,
                              SlugField, TextField, UniqueConstraint)

from users.models import User


class Genre(Model):
    name = CharField(
        verbose_name='Жанр',
        max_length=256,
    )
    slug = SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(Model):
    name = CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = SlugField(
        verbose_name='Слаг категории',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(Model):
    name = CharField(
        verbose_name='Название',
        max_length=256,
    )
    description = TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    year = IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(date.today().year),
        ]
    )
    rating = IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        null=True,
        blank=True,
        default=None,
    )
    genre = ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(Model):
    title = ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=CASCADE,
    )
    text = CharField(
        verbose_name='Текст отзыва',
        max_length=200
    )
    author = ForeignKey(
        User,
        verbose_name='Автор отзыва',
        related_name='reviews',
        on_delete=CASCADE,
    )
    score = IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(Model):
    review = ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=CASCADE
    )
    text = CharField(
        verbose_name='Текст комментария',
        max_length=200
    )
    author = ForeignKey(
        User,
        verbose_name='Автор комментария',
        related_name='comments',
        on_delete=CASCADE
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
