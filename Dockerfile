FROM python:3.11


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app


RUN python -m pip install --upgrade pip
RUN python -m pip install poetry


COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction

COPY docker/entrypoint.sh docker/entrypoint.sh

RUN chmod +x docker/entrypoint.sh

ENTRYPOINT ["docker/entrypoint.sh"]

CMD ["make", "start"]
