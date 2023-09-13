FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip \
                       ca-certificates curl gnupg

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["make", "start"]
