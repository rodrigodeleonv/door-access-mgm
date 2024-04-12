"""This module control the Raspberry Pi GPIO"""
import logging
from time import sleep

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)


def open_door(pin_number: int, time_signal_open: int) -> None:
    """Produce the signal to open the door.

    Args:
        pin_number: GPIO pin number
        time_signal_open: time in seconds to set the pin output high then low.
            Usually 1 second.
    """
    logger.debug("Send signal to Open the door")
    GPIO.output(pin_number, GPIO.HIGH)
    sleep(time_signal_open)
    logger.debug("Stop signal to Open the door")
    GPIO.output(pin_number, GPIO.LOW)


def run():
    from django.conf import settings
    from access_control.rpi_gpio_conf import setup_gpio, cleanup_gpio

    setup_gpio()
    open_door(settings.RPI_GPIO_PIN_OPEN, settings.RPI_TIME_SIGNAL_OPEN)
    cleanup_gpio()
