from rest_framework.serializers import ModelSerializer, CharField

from users.models import User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(ModelSerializer):
    username = CharField(
        required=True)
    confirmation_code = CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
