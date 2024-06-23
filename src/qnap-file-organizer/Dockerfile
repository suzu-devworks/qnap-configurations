FROM python:3-alpine as production
WORKDIR /app

RUN apk add --no-cache --virtual .build-deps build-base jpeg-dev zlib-dev
RUN apk add --no-cache libjpeg-turbo

COPY . .
RUN pip install --no-cache-dir -r requirements.lock

RUN apk del .build-deps

CMD [ "sh", "/app/scripts/exec.sh", "/mnt/dist", "/mnt/source" ]
