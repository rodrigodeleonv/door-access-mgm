"""Raspberry Pi GPIO Configuration.

This module configures the Raspberry Pi GPIO.

In development environment, it's possible that this function can be called multiple times.
with warnings: RuntimeWarning: This channel is already in use, continuing anyway...
because in Django development server (runserver) environment, the server automatically reloads
for many changes, which can cause the ready method of apps to execute more than once

`python proj/manage.py runserver --noreload`

In a production environment, or when running the Django server in a way that doesn't automatically reload
(e.g., using gunicorn or running with python manage.py runserver --noreload), you might not encounter this issue.
However, it's essential to address it properly for development and to ensure clean exits and starts in any environment.
"""

import atexit
import logging

from django.conf import settings
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)


def setup_gpio() -> None:
    """Setup GPIO pins for the project.

    This function must be called only once.
    """

    print("setup the GPIO")
    logger.debug("setup the GPIO")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings.RPI_GPIO_PIN_OPEN, GPIO.OUT)


def cleanup_gpio():
    print("Cleaning up GPIO")
    logger.debug("Cleaning up GPIO")
    GPIO.cleanup()


# Register the GPIO cleanup function to be called at exit
atexit.register(cleanup_gpio)
