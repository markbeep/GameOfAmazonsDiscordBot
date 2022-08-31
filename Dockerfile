FROM alpine:3.16.2

WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache python3
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 bot.py
