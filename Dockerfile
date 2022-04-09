FROM python:3.8.10-alpine

WORKDIR /app
COPY . /app

RUN apk update
RUN apk add --no-cache  gcc \
						musl-dev \
						mariadb-connector-c-dev \
						python3-dev \
						gpgme-dev \
						libc-dev
RUN apk add build-base
RUN rm -rf /var/cache/apk/*

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install setuptools
RUN pip install -r lite_req.txt

ENV FLASK_APP=app_auth
ENV FLASK_DEBUG=1

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80", "--cert=adhoc"]
EXPOSE 80
