FROM ubuntu:20.04
WORKDIR /app
ADD . /app

RUN apt update
RUN apt install -y software-properties-common gnupg wget
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3 python3-pip

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry
RUN poetry install

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org

RUN mkdir -p /data/db

# Set /usr/bin/mongod as the dockerized entry-point application
ENTRYPOINT ["/bin/sh", "scripts/docker_entry_script.sh"]
EXPOSE 8080