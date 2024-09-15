FROM python:alpine3.11 AS python-base

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    nginx \
    openssl-dev \
    make

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY ./docker/nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000

COPY ./docker/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]