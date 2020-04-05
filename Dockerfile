FROM python:alpine3.7


COPY . /app
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev

RUN pip3 install -r prod-requirements.txt

RUN apk del --no-cache .build-deps
CMD [ "python3", "agt-backend-app.py" ]
