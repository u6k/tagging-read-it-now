FROM python:3.8-slim

RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

VOLUME /var/myapp
WORKDIR /var/myapp

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv sync --dev

CMD ["pipenv", "scripts"]