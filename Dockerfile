FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV="production"

EXPOSE 8000

WORKDIR /app

RUN apt update && \
    apt install --no-install-recommends -y build-essential musl-dev ca-certificates && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD [ "sh", "./start.sh" ]