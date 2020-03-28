FROM ubuntu:16.04
g
RUN apt-get update
RUN apt-get install python3-pip
RUN apt-get install flask

RUN pip3 install -r requirements.txt

ADD agt-backend-app.py /

WORKDIR /

CMD [ "python3", "app.py" ]