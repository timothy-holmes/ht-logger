# ht-logger
Consumes webhooks from my baby's room humidity and temperature IoT device (Shelly H&amp;T) and stores in sqlite db.

## To use, follow these steps

Clone to host

```sh
    cd /srv/git
    git clone https://github.com/timothy-holmes/ht-tracker
```

Build and run using docker-compose

```sh
    cd ht-tracker
    docker-compose build
    docker-compose up -d
```

Test app

```sh
    curl http://192.168.1.103:8002/status
    curl http://192.168.1.103:8002/consume?parameter1=100&parameter2=200&parameter3=hahahaha
```

Configure webhook on Shelly H&T device

Wait for the requests (droids) you're looking for...

View chart on iDevice (or similar) here [http://192.168.1.103:8002/last/3/days/]
