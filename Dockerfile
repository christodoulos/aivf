FROM python:3.8-slim-buster
MAINTAINER Christodoulos Fragkoudakis <chfrag@mail.ntua.gr>

ENV INSTALL_PATH /aivf
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "aivf.app:create_app()"
