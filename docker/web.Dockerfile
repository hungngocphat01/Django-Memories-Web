FROM python:3.10.5-alpine3.16
RUN mkdir /root/app
COPY requirements.txt /root/app
COPY ./docker/start-server.sh /root/app/start-server.sh
RUN chmod +x /root/app/start-server.sh
WORKDIR /root/app
RUN apk update
RUN apk add musl-dev postgresql gcc libpq-dev libffi-dev 
RUN pip install -r requirements.txt
COPY source /root/app