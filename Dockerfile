FROM python:alpine3.7


COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD [ "python3", "agt-backend-app.py" ]
