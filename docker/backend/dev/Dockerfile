FROM python:3.10-alpine3.18

COPY ./docker/backend/requirements/requirements.txt .

RUN python3 -m pip install -r requirements.txt

WORKDIR /src

COPY ./src .

WORKDIR /

COPY ./docker/backend/dev/start.sh .

RUN chmod +x start.sh
