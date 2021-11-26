FROM python:3.8-slim
WORKDIR /app
ADD . /app
COPY poetry.lock pyproject.toml /app/

RUN python -m pip install --upgrade pip
RUN pip install poetry

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR /app/hybrid_rs
CMD ["python", "/app/hybrid_rs/server.py"]
EXPOSE 8080