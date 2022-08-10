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

Wait for the requests (droids) you're looking for... While waiting view chart on iDevice (or similar) here [http://192.168.1.103:8002/last/3/days/]. Should show the last 3 days of BOM data.

## next TODO

- DevOps!
  - stop adding features!
  - create 'working' version for current app
    - create a test configuration that works on Windows
      - draw process/architecture diagram
      - database.db.test with sample data
      - tests for more things
      - fix things until working
  - create automated testing environment for Linux
    - docker-compose
      - services
        - cron pulls latest commit from main git branch
          - runs tests
          - generates migration script
          - moves tested source code into app /src volume
          - app uvicorn reloads with new source code and runs migration
        - production app



## misc TODOs

- error visibility through daily email of errors and exceptions
  - logging exceptions and errors
- write more tests. eg. get_n_days() - got error, endpoints
- do a better job managing multiple devices
  - status check query for all devices
  - device metrics (number of check-in)
  - enable multiple BOM stations by getting device list before updating
    - eg. Laverton, Olympic Park, Hobart
- reduce time between BOM updates to 3 hours
- graphing
  - add value labels to last points for each series
  - add gridlines
  - add value labels to graph for local minima/maxima
- controller for smart power point
  - turn on, turn off thresholds/rule manager
  - maybe a new system for managing ops devices
