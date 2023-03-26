from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer, Serializer,
                                        SlugRelatedField)

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UsersSerializer(ModelSerializer):
    """Сериализатор для пользователя с ролью 'moderator', 'admin'."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class NotAdminSerializer(ModelSerializer):
    """Сериализатор для пользователя с ролью 'user'."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class SignUpSerializer(ModelSerializer):
    """Сериализатор для получение кода подтверждения."""
    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(Serializer):
    """Сериализатор для получение JWT-токена."""
    username = CharField(
        max_length=150, validators=[UnicodeUsernameValidator, ]
    )
    confirmation_code = CharField()


class GenreSerializer(ModelSerializer):
    """Сериализатор для всех доступных действий с жанрами."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(ModelSerializer):
    """Сериализатор для всех доступных действий с категориями."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleWriteSerializer(ModelSerializer):
    """Сериализатор для добавления и
    частичного изменения информации о произведении.
    """
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=False,
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'genre',
            'category',
        )


class TitleReadSerializer(ModelSerializer):
    """Сериализатор для всех доступных безопасных методов у произведений."""
    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'year',
            'rating',
            'genre',
            'category',
        )


class ReviewSerializer(ModelSerializer):
    """Сериализатор для всех доступных действий с отывами."""
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise ValidationError('Оценка по 10-бальной шкале.')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв.')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(ModelSerializer):
    """Сериализатор для всех доступных действий с комментариями к отзывам."""
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
