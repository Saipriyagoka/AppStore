FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app_store/ /app_store/logs/

WORKDIR /app_store/

ADD requirements.pip /app_store/

RUN pip install -r requirements.pip

RUN pip install ipython

ADD . /app_store/