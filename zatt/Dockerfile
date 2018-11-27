FROM python:3.5-alpine

EXPOSE 5254
EXPOSE 5255
EXPOSE 5256

COPY . /app/
COPY ./zattstart.sh /app/zattstart.sh
WORKDIR /app

RUN python setup.py install

CMD ["./zattstart.sh"]