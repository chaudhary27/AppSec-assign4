FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3-pip python3

COPY ./requirements.txt /requirements.txt

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 5000

WORKDIR /app

RUN pip3 install -r /requirements.txt

COPY . /app

CMD [ "flask", "run" ]