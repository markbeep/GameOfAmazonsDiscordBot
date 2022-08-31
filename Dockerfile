FROM alpine:3.16.2

WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache python3 gcc python3-dev 
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN apk add --no-cache libc-dev
RUN pip3 install discord-py==1.7.3

COPY . .

CMD python3 bot.py
