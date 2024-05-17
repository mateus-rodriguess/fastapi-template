#!/bin/bash

# Exit in case of error
set -e

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    find . -type d -name __pycache__ -exec rm -r {} \+
fi


pipenv run alembic upgrade head
pipenv run python initial_data.py

environment_var=$(echo $ENVIRONMENT | tr -d '[:space:]')

if [ "$environment_var" = "local" ]; then
    echo "Running in local environment. Performing local actions..."
    pipenv run python main.py
else
    echo "Running in production actions..."
    pipenv run gunicorn main:app --config ./gunicorn_conf.py 
fi