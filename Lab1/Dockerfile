FROM python:3.10

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip3 install nltk

CMD ["python3","main.py"]
