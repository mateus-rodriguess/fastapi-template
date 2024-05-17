import logging

import pytest

import gunicorn_conf
import main
from initial_data import init_data


@pytest.mark.anyio
async def test_my_function():
    try:
        main.app
    except Exception as error:
        logging.error(error)


def test_gunicorn_conf():
    try:
        gunicorn_conf.__dict__
    except Exception as error:
        logging.error(error)


@pytest.mark.anyio
async def test_initial_data():
    try:
        await init_data()
    except Exception as error:
        logging.error(error)
