#FROM python:alpine3.7
FROM python:3.7.1


COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD [ "python3", "agt-backend-app.py" ]
