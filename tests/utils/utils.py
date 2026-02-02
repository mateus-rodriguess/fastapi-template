import random
import string

from app.core.settings import get_settings

settings = get_settings()


def random_email() -> str:
    name = "".join(random.choices(string.ascii_lowercase, k=32))
    return f"{name}@any.com"


def random_password() -> str:
    choice = string.ascii_letters + string.digits + string.punctuation
    return "".join([random.choice(choice) for n in range(12)])


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))
