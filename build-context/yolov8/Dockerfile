FROM python:3.8
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 zip -y

RUN pip install ultralytics

WORKDIR /usr/src/app