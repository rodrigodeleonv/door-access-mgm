"""This module control the Raspberry Pi GPIO

Commented out because it's transicional to remote GPIO control.
"""

import logging
from time import sleep

logger = logging.getLogger(__name__)


def open_door(pin_number: int, time_signal_open: int) -> None:
    """Produce the signal to open the door. Setup the GPIO must occur before.

    WARNING: This functions is blocking operation and can block the server
    for time_signal_open seconds. It's possible to use directly with Django or
    you can configure something like Celery. If you use directly with Django
    remember it block a while the request for  processing in the view.

    Args:
        pin_number: GPIO pin number
        time_signal_open: time in seconds to set the pin output high then low.
            Usually 1 second.
    """
    logger.debug("Send signal to Open the door")
    #
    # TODO: Implement code to open the door
    #
    sleep(time_signal_open)
    logger.debug("Stop signal to Open the door")
    #
    # TODO: Implement code to open the door
    #
    raise NotImplementedError("Implement code to open/close the door")


def run():
    from django.conf import settings
    # from access_control.rpi_gpio_conf import setup_gpio  # , cleanup_gpio

    open_door(settings.RPI_GPIO_PIN_OPEN, settings.RPI_TIME_SIGNAL_OPEN)
