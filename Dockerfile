FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y python3-pip

ADD . /
RUN pip3 install -r requirements.txt

WORKDIR /

CMD [ "python3", "agt-backend-app.py" ]
