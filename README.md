# rakt-test

My solution for [RAKT test task](https://github.com/RAKT-Innovations/P1-django-take-home-assignment).

## Requirements

[Docker](https://docs.docker.com/engine/install/)

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

Note: Authentication is not required for this task. You may simply press ``Try it out`` button, set query parameters if needed and then ``Execute``.

For testing purposes you may take coordinates somewhere in [San Francisco](https://www.google.com/maps/place/San+Francisco,+CA,+USA/@37.75047,-122.4536201,12.75z/data=!4m6!3m5!1s0x80859a6d00690021:0x4a501367f076adff!8m2!3d37.7749295!4d-122.4194155!16zL20vMGQ2bHA?entry=ttu).

**Example**: ``lat=37.775912, lon=-122.450759``
