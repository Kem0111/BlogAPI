#!/bin/bash
poetry run alembic revision --autogenerate -m "create new revision"
poetry run alembic upgrade head
exec "$@"