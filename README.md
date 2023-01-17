# Описание

MultiRecommender представляет собой рекомендательные системы для разного рода медиа-развлечений: фильмы, аниме, игры и т.д. На текущий реализовано только аниме.

Данный репозиторий представляет собой веб-интерфейс для [MultiRecommender](https://github.com/CapBlood/multi-recommender.git).

# Развертывание
Развертывание производится с помощью Docker. Для сборки Docker-образа необходимо в корне проекта выполнить:
```
docker build -t multirecommender .
```

После чего создать контейнер образа и запустить его (порт 8099 можно изменить в `Dockerfile`):
```
docker run --publish 8080:8099 multirecommender
```

Сервер будет доступен на порте 8080.

# Разработка

Перед разработкой необходимо установить Python версии 3.8-3.9, после чего установить Poetry (`pip install poetry`). Затем установить все зависимости проекта:
```
poetry install
```

После чего сервер можно будет запустить через команду `poetry run server`. Однако перед этим необходимо запустить MongoDB и указать его IP и порт в конфигурационном файле `hybrid_rs/server/config.toml`. Также необходимо инициализировать MongoDB с помощью скрипта `scripts/init_db.sh`.

**Примечание:** для режима отладки сервера необходимо запустить команду `poetry run debug`.