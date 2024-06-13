#!/bin/bash

# Exit in case of error
set -e

pipenv run alembic upgrade head
pipenv run python initial_data.py

ENVIRONMENT=$(echo "$ENVIRONMENT" | tr -d '[:space:]')

if [ "$ENVIRONMENT" = "local" ]; then
    echo "Running in local environment. Performing local actions..."
    pipenv run python main.py
else
    echo "Running in production actions..."
    pipenv run gunicorn main:app --config ./gunicorn_conf.py 
fi