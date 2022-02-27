# Cloud Book Writer Platform Backend

A platform where users can write books and save it on cloud without keeping files stored locally. Users can collaborate
with other writers as well on the same book without thinking too much about the collaboration process.

**Requirements:** Please see attached Google
Docs [link](https://docs.google.com/document/d/19aeJIJmxPpaad6xSRoT92cCmtR2HvOfE4BulK8_HdF0) for detailed
specifications.

**Docs**: Please view [docs](docs/README.md) folder to read about design and development decisions.

## Getting Started

### Setup using virtualenv

1. Create virtualenv using the below command:

```shell
$ virtualenv venv
```

2. Install requirements

```shell
$ pip install -r requirements.txt
```

3. Test server.

```shell
$ cd src
$ python manage.py test
```

4. Run server. The development server should be live at localhost:8000.

```shell
$ python manage.py runserver
```

### Setup using docker compose

1. Install docker using the [official documentation](https://docs.docker.com/get-docker/)
2. Use the following command to run tests using docker compose:

```shell
$ docker compose -f docker-compose.test.yaml up
```

3. Use the following command to run server. The development server should be live at localhost:8000.

```shell
$ docker compose up
```

## Changelog

Please read [CHANGELOG](CHANGELOG.md) to view development progress.

## License

[MIT](LICENSE)
