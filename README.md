# Shift

[Built with Cookiecutter DjangoRestFramework](https://github.com/PC-Nazarka/cookiecutter-django-rest-framework/)

## Запуск проекта

Перед запуском проекта нужно создать ``.env`` файл на основе ``.env.template`` и добавить в ``.env`` следующие переменные:

- DJANGO_EMAIL_HOST
- DJANGO_EMAIL_PORT
- DJANGO_EMAIL_HOST_USER
- DJANGO_EMAIL_HOST_PASSWORD

Для запуска проекта требуется установленный docker-compose.

## DEV

Команда для запуска:

```bash
docker-compose up --build --remove-orphans
```

Команда для применения миграций:

```bash
docker-compose exec django python manage.py migrate
```

Команда для создания админа (супер пользователя):

```bash
docker-compose exec django python manage.py createsuperuser
```

## PROD

Команда для запуска prod версии:

```bash
docker-compose -f docker-compose.prod.yml up --build --remove-orphans
```

Команда для применения миграций:

```bash
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate
```

Команда для создания админа (супер пользователя):

```bash
docker-compose -f docker-compose.prod.yml exec django python manage.py createsuperuser
```