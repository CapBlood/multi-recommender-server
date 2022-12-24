FROM ubuntu:20.04
WORKDIR /app

# Установка Python и Poetry
RUN apt update
RUN apt install -y software-properties-common gnupg wget
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3 python3-pip

RUN pip install poetry

# Установка MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org

RUN mkdir -p /data/db

# Установка Nginx
RUN apt install -y nginx

RUN apt install -y vim

# Установка сервера
ADD . /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN ["/bin/sh", "/app/scripts/init_nginx.sh"]
RUN ["/bin/sh", "/app/scripts/init_db.sh"]

# Set /usr/bin/mongod as the dockerized entry-point application
ENTRYPOINT ["/bin/sh", "/app/scripts/docker_entry_script.sh"]
EXPOSE 80
CMD ["poetry", "run", "run-server"]
