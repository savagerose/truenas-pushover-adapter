FROM alpine:latest

RUN apk add --update --no-cache python3 py3-aiohttp

WORKDIR /app
COPY truenas-pushover.py ./

CMD ["/usr/bin/env", "python3", "-u", "truenas-pushover.py"]
