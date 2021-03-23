FROM golang:alpine AS go_build
WORKDIR /go/src/github.com/adnanh/webhook
ENV WEBHOOK_VERSION 2.8.0
RUN apk add --update -t build-deps curl libc-dev gcc libgcc
RUN curl -L --silent -o webhook.tar.gz https://github.com/adnanh/webhook/archive/${WEBHOOK_VERSION}.tar.gz && \
    tar -xzf webhook.tar.gz --strip 1 &&  \
    go get -d && \
    go build -o /usr/local/bin/webhook && \
    apk del --purge build-deps && \
    rm -rf /var/cache/apk/* && \
    rm -rf /go

FROM python:alpine AS python_build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --update --no-cache gcc musl-dev

COPY requirements.txt requirements.txt

RUN python -m venv $VIRTUAL_ENV \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=python_build $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=go_build /usr/local/bin/webhook /usr/local/bin/webhook
COPY /benzaiten /var/scripts/

RUN chmod +x /var/scripts/conduit.py \
    && chmod +x /var/scripts/dockerhub.py \
    && chmod +x /var/scripts/webactivity.py \
    && chmod +x /var/scripts/phabricator.sh \
    && chmod +x /var/scripts/dockerhub.sh
    
EXPOSE 9000

CMD [ "/usr/local/bin/webhook", "-verbose", "-hooks=/var/scripts/hooks.json", "-hotreload" ]
