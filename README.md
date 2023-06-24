# Shift

[Built with Cookiecutter DjangoRestFramework](https://github.com/PC-Nazarka/cookiecutter-django-rest-framework/)

## Запуск проекта

Для запуска проекта требуется установленный docker-compose.

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