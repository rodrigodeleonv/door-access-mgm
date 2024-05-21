"""This module control the Raspberry Pi GPIO

Test open the door.
"""

import logging
from time import sleep

from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

from access_control.rpi_gpio_conf import get_door

logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


def remote_create(ip: str, pin: int) -> None:
    """Create a remote GPIO handler as a example.

    Args:
        ip: IP address of the remote GPIO server.
        pin: GPIO pin number.
    """
    logger.info(f"Testing remote GPIO. Use LED and PiGPIOFactory: {ip}, pin {pin}")
    factory = PiGPIOFactory(ip)
    door = LED(pin, pin_factory=factory)
    door.on()
    sleep(1)
    door.off()


def remote_defaults():
    door = get_door()
    logger.info(
        f"Testing remote GPIO. Use DoorPinGPIO, defaults: {door.gpio_hostname}, pin {door.door_pin}"
    )
    while True:
        try:
            door.open_door()
        except KeyboardInterrupt:
            door.cleanup()
            break


def run():
    remote_defaults()
    # remote_create("172.17.0.1", 17)
