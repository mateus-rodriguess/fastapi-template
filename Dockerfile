FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000 80 443 22

WORKDIR /app

RUN apt update && \
    apt install --no-install-recommends -y build-essential musl-dev ca-certificates && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install pipenv
RUN pipenv install

CMD [ "bash", "./start.sh" ]