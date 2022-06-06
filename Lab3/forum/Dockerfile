FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /forum
WORKDIR /forum
COPY requirements.txt /forum/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /forum/