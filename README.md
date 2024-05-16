# Web Door Access Management

Web interface to configure Laboratory door access.
This web application is made for Raspberry Pi devices. It use the GPIOs.

Features:

- Admin interface to manage Users, RFID Tags, ...
- API to conect with external RDIF Reader service

![Diagram 1](/docs/images/lab-door-system.drawio.png)

## Install

Docker & Docker compose

```bash

git clone https://github.com/rodrigodeleonv/door-access-mgm.git
docker compose pull

# Previous steps

## MANDATORY: generate a secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

## MANDATORY: create .prod.env and modify the values
cp example.env .prod.env
## Recommended edit `.prod.env` and add superuser email and password

## Optional Provisioning: just for the first time
## Provision RFID tags
## folder: ./provision/
cp provision/tags.example.json provision/tags.json
vi provision/tags.json

## Deploy
docker compose --env-file .prod.env up -d
```

## Dev

Ensure you have Qemu

```bash
docker run --privileged --rm tonistiigi/binfmt --install all
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
ls -lha /proc/sys/fs/binfmt_misc/qemu-*
docker buildx ls
```

Ref:
- <https://stackoverflow.com/questions/66116587/docker-buildx-mulitarch-armv6>
- <https://docs.docker.com/build/building/multi-platform/>
- <https://collabnix.com/building-arm-based-docker-images-on-docker-desktop-made-possible-using-buildx/#Introducing_buildx>
- <https://devopstales.github.io/linux/running_and_building_multi_arch_containers/>

Remote GPIOs: <https://gpiozero.readthedocs.io/en/stable/remote_gpio.html>

```bash
# Docker

## Build & tag image, use buidlx for armv6 and armv8
## Tag production: to deploy to production
## Raspberry Pi 1B with arm6l (32bits)
poetry export -f requirements.txt --output requirements-prod.txt --without-hashes
docker buildx build --platform linux/arm/v6,linux/arm64 \
    -t rodmosh/door-access-mgm:rpi-0.2.1 \
    -t rodmosh/door-access-mgm:production \
    --push .

## use --load for add to local registry or --push
# docker buildx build --platform linux/arm/v6 -t rodmosh/door-access-mgm:rpi-0.2.1 --load .
# docker buildx build --platform linux/arm64 -t rodmosh/door-access-mgm:rpi-0.2.1 --push .

## Test architecture (in your x64 processor)
docker run -e QEMU_CPU=arm1176 --platform linux/arm/v6 --rm -it python:3.11.9-slim-bullseye uname -m
docker run -e QEMU_CPU=arm1176 --platform linux/arm/v6 --rm -it rodmosh/door-access-mgm:rpi-0.2.1 uname -m
docker run --platform linux/arm64 --rm -it python:3.11.9-slim-bullseye bash
docker run --platform linux/arm/v8 --rm -it python:3.11.9-slim-bullseye bash
docker run --rm -it -e ENTRY_SKIP=1 rodmosh/door-access-mgm:production bash

## Clean cache
docker buildx prune -f

# PostreSQL
docker run --rm --name pg \
    -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres \
    -p 5432:5432 -d \
    postgres:16-alpine

# Django
docker run --privileged --rm -p 8000:8000 \
    --device /dev/gpiomem \
    -e DJANGO_SECRET_KEY='django-insecure-yck2)0pdsmgl=!&l*1t0w5!6h9)*@*&v)$%a8(07@8-+=!gvd9' \
    -e DJANGO_ALLOWED_HOSTS='*' \
    rodmosh/door-access-mgm:production gunicorn --pythonpath ./proj proj.wsgi --bind 0.0.0.0:8000


# Local Dev

docker compose -f compose.local.yml up -d
python proj/manage.py migrate
python proj/manage.py runserver 0.0.0.0:8000
```

## Notes with Raspberry Pi and GPIO

Docker Access to Raspberry Pi GPIO Pins
<https://stackoverflow.com/questions/30059784/docker-access-to-raspberry-pi-gpio-pins>


## (Gnome) Keyring

Some problems can occur with poetry and gnome kerying in development machine. In that case, you should disable kerying
<https://github.com/python-poetry/poetry/issues/8623>

```bash
export PYTHON_KEYRING_BACKEND="keyring.backends.fail.Keyring"

# for permanent add this to ~/.bashrc
```

## Qemu

[qemu: uncaught target signal 11 (Segmentation fault) - core dumped](https://github.com/docker/buildx/issues/1170)

## Remote GPIO

<https://gpiozero.readthedocs.io/en/latest/remote_gpio.html>

```bash
# Use flags -n -l, only allows specific or localhost
# use no flags or foreground -g, it will allow remote connections
sudo pigpiod -g

# Service file has -l, that allows only local by default
# https://raspberrypi.stackexchange.com/a/104441
cat /lib/systemd/system/pigpiod.service
```

[How to Run pigpiod on boot](https://raspberrypi.stackexchange.com/questions/70568/how-to-run-pigpiod-on-boot)

```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
sudo pigpiod

sudo netstat -tunpl

sudo systemctl disable pigpiod
sudo systemctl stop pigpiod
```