FROM alpine:latest

RUN apk add --no-cache bash curl

COPY simulate-requests.sh /simulate-requests.sh

RUN chmod +x /simulate-requests.sh

CMD ["bash", "/simulate-requests.sh"]
