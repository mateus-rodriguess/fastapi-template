<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>

<p align="center">
  <a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
      <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
  </a>
  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
      <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/fastapi" target="_blank">
      <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
  </a>
</p>

The `FastAPI` template is a template repository for microservices. In this template, you will find examples of how to build a robust application with FastAPI.

## Technology Stack and Features
- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
  - 🚀 Fast: Supports async/await syntax for routes and database connection.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
  - 💪 Robust: Get production-ready code with automatic interactive documentation.
  - 🔐 Security: `OAuth2` with `fastapi.security`

- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- ✅ [pytest](https://docs.pytest.org/en/8.0.x/) Unitary tests.
- 🧰 [alembic](https://alembic.sqlalchemy.org/en/latest/) Database migrations.
- 🔒 Secure password hashing by default.
- 🔑 JWT token authentication.
- 🚢 Deployment instructions using Docker Compose.
- 📑 Color logger translator with `guvicorn-logger`.
- 📑 Pagination: `fastapi-pagination` to simplify pagination.


### Interactive API Documentation
  Get production-ready code with automatic interactive documentation.
  API documentation at [Docs](http://127.0.0.1:8000/docs)

  [![API docs](img/docs.png)](https://github.com/mateus-rodriguess/fastapi-back-end-template)


## How To Use It

You can **just fork or clone** this repository and use it as is.

✨ It just works. ✨

### How to Use a Private Repository

If you want to have a private repository, GitHub won't allow you to simply fork it as it doesn't allow changing the visibility of forks.

But you can do the following:

- Create a new GitHub repo, for example `my-back-end`.
- Clone this repository manually, set the name with the name of the project you want to use, for example `my-back-end`:

  ```bash
  git clone git@github.com:mateus-rodriguess/fastapi-back-end-template.git my-back-end
  ```

- Enter into the new directory:

  ```bash
  cd my-back-end
  ```

- Set the new origin to your new repository, copy it from the GitHub interface, for example:

  ```bash
  git remote set-url origin git@github.com:mateus-rodriguess/fastapi-back-end-template.git
  ```

- Add this repo as another "remote" to allow you to get updates later:

  ```bash
  git remote add upstream git@github.com:mateus-rodriguess/fastapi-back-end-template.git
  ```

- Push the code to your new repository:

  ```bash
  git push -u origin main
  ```

## Migrations

  ```bash
  # Create a model in app/models
  # Create a migration file
  $ alembic revision --autogenerate -m "Migration message."
  $ alembic upgrade head

  ```

## License

This project is licensed under the terms of the MIT license.
