from rest_framework.serializers import ModelSerializer
from reviews.models import Category, Genre, Title
from users.models import User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class NotAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('role',)


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(ModelSerializer):
    class Meta:
        model = Title
        fields = (
            'name',
            'description',
            'year',
            'rating',
            'genre',
            'category',
        )
