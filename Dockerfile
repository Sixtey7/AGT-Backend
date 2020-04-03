FROM python:alpine3.7


COPY . /
WORKDIR /
RUN pip3 install -r requirements.txt

WORKDIR /

CMD [ "python3", "agt-backend-app.py" ]
