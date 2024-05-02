# Web Door Access Management

Web interface to configure Laboratory door access.
This web application is made for Raspberry Pi devices. It use the GPIOs.

Features:

- Admin interface to manage Users, RFID Tags, ...
- API to conect with external RDIF Reader service

![Diagram 1](/docs/images/lab-door-system.drawio.png)

## Install

## Dev

```bash
# Build image
poetry export -f requirements.txt --output requirements-prod.txt --without-hashes
python proj/manage.py collectstatic --noinput
docker build -t rodmosh/door-access-mgm .
docker run --privileged --rm -p 8000:8000 \
    --device /dev/gpiomem \
    -e DJANGO_SECRET_KEY='django-insecure-yck2)0pdsmgl=!&l*1t0w5!6h9)*@*&v)$%a8(07@8-+=!gvd9' \
    -e DJANGO_ALLOWED_HOSTS='*' \
    rodmosh/door-access-mgm gunicorn --pythonpath ./proj proj.wsgi --bind 0.0.0.0:8000

# Dev webserver
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
