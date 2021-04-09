FROM python:3.8-alpine

LABEL MAINTAINER="M. Mustafa Aydin <mma-95@hotmail.com>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD requirements.txt /var/www/
RUN apk add gcc musl-dev libffi-dev
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi", "--reload"]
