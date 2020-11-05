FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y wget ca-certificates
RUN apt-get install -y gnupg2
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt focal-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update -y
RUN apt install -y postgresql
RUN service postgresql start
COPY info/requirements.txt requirements.txt
RUN apt-get install -y python3-pip
RUN apt-get install -y libpq-dev
RUN pip3 install -r requirements.txt

COPY info/ app/
COPY connection/ connection/
RUN ls app
RUN python3 app/wsgi.py

