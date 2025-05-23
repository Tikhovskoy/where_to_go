# Where to Go

Демонстрационный сайт с картой интересных мест Москвы. Реализован на Django + Leaflet + Vue.

## Содержание

* [Описание проекта](#описание-проекта)
* [Установка и запуск](#установка-и-запуск)
* [Сценарии использования](#сценарии-использования)
* [API и эндпоинты](#api-и-эндпоинты)
* [Администрирование](#администрирование)
* [Переменные окружения](#переменные-окружения)

## Описание проекта

Этот проект демонстрирует интерактивную карту Москвы с отмеченными локациями. Каждая локация содержит краткое и полное описание, а также галерею изображений, управляемую через админку.

Реализовано:

* Django-приложение `places` с моделями Place и PlaceImage
* Админ-контролли с drag-and-drop сортировкой и предпросмотром изображений
* WYSIWYG-редактор TinyMCE для HTML-описаний
* Статическая карта на Leaflet и Vue.js интерфейс
* JSON API endpoint для получения деталей локации
* Конфигурация settings.py через переменные окружения

## Установка и запуск

1. Клонируем репозиторий:

   ```bash
   git clone https://github.com/<your-username>/where_to_go.git
   cd where_to_go
   ```
2. Настраиваем виртуальное окружение:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Локальные настройки (необязательно):

   ```bash
   export DEBUG=True
   export SECRET_KEY="super-secret-key"
   ```
4. Применяем миграции и создаём суперпользователя:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Запуск сервера:

   ```bash
   python manage.py runserver
   ```
6. Открываем в браузере [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Сценарии использования

1. **Просмотр карты**

   * Открыть главную страницу
   * Взаимодействовать с метками: клик по значку открывает боковую панель
2. **Получение API-данных**

   * Перейти по адресу `/places/<id>/` чтобы получить JSON-описание локации
3. **Администрирование данных**

   * Зайти в `/admin/` под суперпользователем
   * Управлять локациями и изображениями через `places` раздел
   * Добавлять изображения drag-and-drop, редактировать HTML-описания с TinyMCE

## API и эндпоинты

* `GET /places/<id>/` — возвращает JSON:

  ```json
  {
    "title": "...",
    "imgs": ["/media/place_images/1.jpg", ...],
    "description_short": "...",
    "description_long": "..."
  }
  ```

## Администрирование

* Управление локациями: поля `title`, `latitude`, `longitude`, `description_short`, `description_long` (TinyMCE).
* Inline управление изображениями с предпросмотром и drag-and-drop упорядочиванием.

## Импорт данных

### Загрузка одного места

Для загрузки одной локации из JSON-файла используйте встроенную Django-команду `load_place`:

```bash
python manage.py load_place https://example.com/places/moscow_legends.json
````

### Массовая загрузка всех мест из каталога на GitHub

Чтобы загрузить все локации сразу из каталога JSON-файлов (например, из репозитория на GitHub):

```bash
python manage.py load_places_all https://api.github.com/repos/devmanorg/where-to-go-places/contents/places
```

> Для запуска команд необходимо, чтобы у вас был запущен сервер и применены миграции.

## Переменные окружения

| Переменная      | Описание                                  | По умолчанию           |
| --------------- | ----------------------------------------- | ---------------------- |
| `SECRET_KEY`    | Секретный ключ Django                     | `django-insecure-...`  |
| `DEBUG`         | Режим отладки (`True`/`False`)            | `False`                |
| `ALLOWED_HOSTS` | Список хостов (через запятую)             | пустой                 |
| `DATABASE_URL`  | URL базы данных (Postgres, SQLite и т.д.) | `sqlite:///db.sqlite3` |
| `TIME_ZONE`     | Часовой пояс                              | `UTC`                  |

## Демо-сайт

Проект развернут на PythonAnywhere:  
[https://tikhovskoi.pythonanywhere.com](https://tikhovskoi.pythonanywhere.com)