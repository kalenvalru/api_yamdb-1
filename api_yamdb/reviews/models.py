import datetime

from django.core import validators
from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        self.slug


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        self.name


class Title(models.Model):
    description = models.TextField(
        verbose_name='Описание',
        null=True,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            validators.MaxValueValidator(datetime.date.today().year),
        ]
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    rating = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10),
        ],
        null=True,
        default=None,
    )
    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
    
    def __str__(self):
        return self.name
