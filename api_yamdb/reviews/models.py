import datetime

from django.core import validators
from django.db import models


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        max_length=50,
    )
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        max_length=50,
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            validators.MaxValueValidator(datetime.date.today().year),
        ]
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10),
        ],
        null=True,
        blank=True,
        default=None,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
    
    def __str__(self):
        return self.name
