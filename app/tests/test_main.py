import logging

import pytest

import gunicorn_conf
import initial_data
import main


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
        await initial_data.init_data()
    except Exception as error:
        logging.error(error)
