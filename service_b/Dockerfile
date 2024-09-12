FROM golang:1.23.1-alpine AS build

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -o main .

FROM alpine:3.20.3

ENV USER=api-gateway-user
ENV APP_DIR=/home/$USER

RUN addgroup -S $USER && adduser -S $USER -G $USER

WORKDIR $APP_DIR

COPY --from=build /app/main .

RUN chown -R "$USER":"$USER" $APP_DIR

USER $USER

CMD ["./main"]
