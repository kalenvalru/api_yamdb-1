# YaMDb API 
Проект __YaMDb__ собирает отзывы пользователей на различные произведения. 


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/esaviv/api_final_yatube.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv | python -m venv venv
```

```
source env/bin/activate | source venv/Scripts/activate
```

```
python3 -m pip install --upgrade pip | python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate | python manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver | python3 manage.py runserver
```
## Авторы
@esaviv @RoutTufuch @Zhenia1997

## Алгоритм регистрации пользователей:

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами ```email``` и ```username``` на эндпоинт ```/api/v1/auth/signup/```.
2. __YaMDB__ отправляет письмо с кодом подтверждения (```confirmation_code```) на адрес ```email```.
3. Пользователь отправляет POST-запрос с параметрами ```username``` и ```confirmation_code``` на эндпоинт ```/api/v1/auth/token/```, в ответе на запрос ему приходит ```token``` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт ```/api/v1/users/me/``` и заполняет поля в своём профайле (описание полей — в документации).


## Пользовательские роли:

- __Аноним__ — может просматривать описания произведений, читать отзывы и комментарии.
- __Аутентифицированный пользователь__ (```user```) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- __Модератор__ (```moderator```) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- __Администратор__ (```admin```) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- __Суперюзер Django__ — обладет правами администратора (```admin```).


## Примеры запросов и ответов:

### _AUTH_
_Регистрация пользователей и выдача токенов._

### Регистрация нового пользователя
Получить код подтверждения на переданный ```email```. Права доступа: __Доступно без токена__. Использовать имя 'me' в качестве username запрещено. Поля ```email``` и ```username``` должны быть уникальными.
#### POST
```
/api/v1/auth/signup/
```
```
{
  "email": "user@example.com",
  "username": "string"
}
```
Ответ:
```
{
  "email": "string",
  "username": "string"
}
```

### Получение JWT-токена
Получение JWT-токена в обмен на username и confirmation code. Права доступа: __Доступно без токена__.
#### POST
```
/api/v1/auth/token/
```
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
Ответ:
```
{
  "token": "string"
}
```


### _USERS_
_Пользователи_.

### Получение списка всех пользователей
Получить список всех пользователей. Права доступа: __Администратор__
#### GET
```
/api/v1/users/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```

### Добавление пользователя
Добавить нового пользователя. Права доступа: __Администратор__ Поля ```email``` и ```username``` должны быть уникальными.
#### POST
```
/api/v1/users/
```
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Получение пользователя по username
Получить пользователя по username. Права доступа: __Администратор__
#### GET
```
/api/v1/users/{username}/
```
Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Изменение данных пользователя по username
Изменить данные пользователя по username. Права доступа: __Администратор__. Поля ```email``` и ```username``` должны быть уникальными.
#### PATCH
```
/api/v1/users/{username}/
```
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Удаление пользователя по username
Удалить пользователя по username. Права доступа: __Администратор__.
#### DELETE
```
/api/v1/users/{username}/
```

### Получение данных своей учетной записи
Получить данные своей учетной записи Права доступа: __Любой авторизованный пользователь__.
#### GET
```
/api/v1/users/me/
```
Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Изменение данных своей учетной записи
Изменить данные своей учетной записи. Права доступа: __Любой авторизованный пользователь__. Поля ```email``` и ```username``` должны быть уникальными.
#### PATCH
```
/api/v1/users/me/
```
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### _TITLES_
_Произведения, к которым пишут отзывы (определённый фильм, книга или песенка)_.

### Получение списка всех произведений
Получить список всех объектов. Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/titles/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

### Добавление произведения
Добавить новое произведение. Права доступа: __Администратор__. Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего). При добавлении нового произведения требуется указать уже существующие категорию и жанр.
#### POST
```
/api/v1/titles/
```
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

### Получение информации о произведении
Информация о произведении. Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/titles/{titles_id}/
```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

### Частичное обновление информации о произведении
Обновить информацию о произведении. Права доступа: __Администратор__.
#### PATCH
```
/api/v1/titles/{titles_id}/
```
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

### Удаление произведения
Удалить произведение. Права доступа: __Администратор__.
#### DELETE
```
/api/v1/titles/{titles_id}/
```


### _GENRES_
_Категории жанров_.

### Получение списка всех жанров
Получить список всех жанров. Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/genres/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Добавление жанра
Добавить жанр. Права доступа: __Администратор__. Поле ```slug``` каждой категории должно быть уникальным.
#### POST
```
/api/v1/genres/
```
```
{
  "name": "string",
  "slug": "string"
}
```
Ответ:
```
{
  "name": "string",
  "slug": "string"
}
```

### Удаление жанра
Удалить жанр. Права доступа: __Администратор__.
#### DELETE
```
/api/v1/genres/{slug}/
```


### _CATEGORIES_
_Категории (типы) произведений_.

### Получение списка всех категорий
Получить список всех категорий Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/categories/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Добавление новой категории
Создать категорию. Права доступа: __Администратор__. Поле ```slug``` каждой категории должно быть уникальным.
#### POST
```
/api/v1/users/
```
```
{
  "name": "string",
  "slug": "string"
}
```
Ответ:
```
{
  "name": "string",
  "slug": "string"
}
```

### Удаление категории
Удалить категорию. Права доступа: __Администратор__.
#### DELETE
```
/api/v1/categories/{slug}/
```


### _REVIEWS_
_Отзывы_.

### Получение списка всех отзывов
Получить список всех отзывов. Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/titles/{title_id}/reviews/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Добавление нового отзыва
Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение. Права доступа: __Аутентифицированные пользователи__.
#### POST
```
/api/v1/titles/{title_id}/reviews/
```
```
{
  "text": "string",
  "score": 1
}
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Полуение отзыва по id
Получить отзыв по id для указанного произведения. Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Частичное обновление отзыва по id
Частично обновить отзыв по id. Права доступа: __Автор отзыва, модератор или администратор__.
#### PATCH
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```
```
{
  "text": "string",
  "score": 1
}
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Удаление отзыва по id
Удалить отзыв по id Права доступа: __Автор отзыва, модератор или администратор__.
#### DELETE
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```


### _COMMENTS_
_Комментарии к отзывам_.

### Получение списка всех комментариев к отзыву
Получить список всех комментариев к отзыву по id. Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Добавление комментария к отзыву
Добавить новый комментарий для отзыва. Пользователь может оставить только один отзыв на произведение. Права доступа: __Аутентифицированные пользователи__.
#### POST
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
{
  "text": "string"
}
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Получение комментария к отзыву
Получить комментарий для отзыва по id. Права доступа: __Доступно без токена__.
#### GET
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Частичное обновление комментария к отзыву
Частично обновить комментарий к отзыву по id. Права доступа: __Автор отзыва, модератор или администратор__.
#### PATCH
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
```
{
  "text": "string"
}
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Удаление комментария к отзыву
Удалить комментарий к отзыву по id. Права доступа: __Автор отзыва, модератор или администратор__.
#### DELETE
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
