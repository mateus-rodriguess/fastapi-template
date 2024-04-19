#!/bin/sh

# Exit in case of error
set -e

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    find . -type d -name __pycache__ -exec rm -r {} \+
fi

# Run migrations
alembic upgrade head

# Create initial data in DB
python initial_data.py

gunicorn main:app --config ./gunicorn_conf.py 
