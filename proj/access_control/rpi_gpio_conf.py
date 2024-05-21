"""Raspberry Pi GPIO Configuration."""

import logging
from time import sleep

from django.conf import settings
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

logger = logging.getLogger(__name__)


class Singleton(type):
    """Singleton class"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DoorPinGPIO(metaclass=Singleton):

    def __init__(
        self, door_pin: int, gpio_hostname: str, time_signal_open: int
    ) -> None:
        """Singleton class to control the Raspberry Pi GPIO.

        It's required to active the service for the Raspberry Pi GPIO:
        - `sudo pigpiod`, no daemon.
        - or `sudo systemctl start pigpiod` for deaemon. Read the pigpiod documentation.

        Args:
            door_pin: GPIO pin number
            gpio_hostname: hostname or IP address of the remote GPIO server.
                example: 127.0.0.1
            time_signal_open: time in seconds to set the pin output high then low.
                Usually 1 second.
        """
        self.door_pin = door_pin
        self.gpio_hostname = gpio_hostname
        self.time_signal_open = time_signal_open

        self.factory = PiGPIOFactory(gpio_hostname)
        self.door = LED(settings.RPI_GPIO_PIN_OPEN, pin_factory=self.factory)

    def __del__(self):
        self.cleanup()

    def open_door(self) -> None:
        """Open the door in a blocking fashion."""
        logger.debug("Opening door")
        self.door.on()
        sleep(self.time_signal_open)
        self.door.off()
        sleep(self.time_signal_open)
        self.door.on()

    def cleanup(self) -> None:
        """Ensure set level to low.

        Require to register this method in apps.py use atexit.
        """
        logger.info("Clean up GPIO: set level to low")
        try:
            self.door.off()
        except AttributeError as e:
            logger.error(f"No clean up made: {e}")


def get_door() -> DoorPinGPIO:
    """Shortcut. Use default settings to create the DoorPinGPIO.

    .. code-block:: python

        door = get_door()

    Returns:
        DoorPinGPIO singleton

    Raises:
        AttributeError if no connection to remote GPIO server.
    """
    return DoorPinGPIO(
        settings.RPI_GPIO_PIN_OPEN,
        settings.RPI_REMOTE_GPIO_HOSTNAME,
        settings.RPI_TIME_SIGNAL_OPEN,
    )
