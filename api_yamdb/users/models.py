import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, TextField, UUIDField

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
    )
    username = CharField(
        'Имя пользователя',
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = TextField(
        'Биография',
        blank=True,
    )
    role = CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    confirmation_code = UUIDField(
        'Код для получения/обновления токена',
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
