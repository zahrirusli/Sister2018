FROM python:3.5-alpine

ADD . /app/
WORKDIR /app

RUN python setup.py install

EXPOSE 5254
CMD ["zattd", "-c", "/app/zatt.conf", "-s", "storage.persist"]