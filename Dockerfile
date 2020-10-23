FROM python:3.8

RUN apt-get update

RUN mkdir /code

ADD . /code

WORKDIR /code

RUN pip install -r /code/requirements.txt

CMD uvicorn --host 0.0.0.0 app:app --reload