FROM python:3.10.5-alpine3.16

ENV APP /root/app/

# Install neccessary packages
RUN mkdir -p $APP
RUN apk update
RUN apk add sudo musl-dev postgresql gcc libpq-dev libffi-dev

# Copy files into image
COPY requirements.txt $APP/requirements.txt
COPY ./docker/django/start-server.sh $APP/start-server.sh

# Copy django project
COPY source $APP

# Install python packages
WORKDIR $APP
RUN pip install -r requirements.txt

# Entry point
CMD [ "/bin/sh", "start-server.sh" ]