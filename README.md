# rakt-test

## Requirements

[Docker]()
[docker compose]()

## Setup

Build docker images

```shell
docker compose build
```

Start container with Database and wait ~10 seconds

```shell
docker compose up -d db
```

Then apply migrations, run tests to check application and load data from CSV file

```shell
docker compose run app python manage.py migrate
docker compose run app python manage.py test
docker compose run app python manage.py load_data food-truck-data.csv
```

Finally start application

```shell
docker compose up -d app
```

And open [Swagger](http://127.0.0.1:8000/swagger/) or [Redoc](http://127.0.0.1:8000/redoc/)
in your browser to see API documentation.

## Get your current location

https://www.gps-coordinates.net/my-location
