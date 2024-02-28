FROM oven/bun:alpine
RUN apk add --no-cache openjdk8-jre
WORKDIR /app
ADD . /app
ENV PORT=80
CMD ["/usr/local/bin/bun", "server.ts"]