from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, Review
from users.models import User
from .filters import FilterTitleSet

from .permissions import (IsAdminOnlyPermission, IsAdminOrReadOnlyPermission,
                          SelfEditUserOnlyPermission, IsAuthorModeratorAdminOrReadOnlyPermission)
from .serializers import (CategorySerializer, GenreSerializer,
                          NotAdminSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UsersSerializer,
                          CommentSerializer, ReviewSerializer)
from .mixins import GetListCreateDeleteViewSet


class SignUpViewSet(APIView):
    """Получение кода подтверждения на переданный email."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if (User.objects.filter(username=request.data.get('username'),
                                email=request.data.get('email'))):
            user = User.objects.get(username=request.data.get('username'))
            serializer = SignUpSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        send_mail(
            subject='Код подтверждения для доступа к API YaMDb.',
            message=(
                f'Здравствуйте!\n\n'
                f'Ваш confirmation_code: {user.confirmation_code}\n'
                f'Он необходим для получения и последующего обновления токена '
                f'по адресу api/v1/auth/token/.'
            ),
            from_email='support@yamdb.com',
            recipient_list=[request.data.get('email')],
            fail_silently=False,
        )
        return Response(
            serializer.data, status=HTTP_200_OK
        )


class TokenViewSet(APIView):
    """Получение JWT-токена в обмен на username и confirmation code."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if str(user.confirmation_code) == request.data.get(
            'confirmation_code'
        ):
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(
                token, status=HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения.'},
            status=HTTP_400_BAD_REQUEST
        )


class UsersViewSet(ModelViewSet):
    """Получение и редактирование информации о пользователе,
    удаление пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOnlyPermission,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(SelfEditUserOnlyPermission,)
    )
    def me_user(self, request):
        if request.method == 'GET':
            user = User.objects.get(username=request.user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        user = User.objects.get(username=request.user)
        serializer = NotAdminSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterTitleSet

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update',):
            return TitleWriteSerializer
        return TitleReadSerializer


class CategoryViewSet(GetListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'slug',)
    lookup_field = 'slug'


class GenreViewSet(GetListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
