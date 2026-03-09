FROM python:3.13.11-alpine
LABEL maintainer="Throwawaychris"

LABEL build_date="2026-01-07"
RUN apk update && apk upgrade
RUN apk add --no-cache git make build-base linux-headers
WORKDIR /discord_bot
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "main.py"]