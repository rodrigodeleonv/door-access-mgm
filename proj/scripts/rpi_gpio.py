"""This module control the Raspberry Pi GPIO

Commented out because it's transicional to remote GPIO control.
"""

import logging

from access_control.rpi_gpio_conf import get_door

logger = logging.getLogger(__name__)


def run():
    logger.info("Testing GPIO PIN(s)")
    door = get_door()
    # door.open_door()
    while True:
        try:
            door.open_door()
        except KeyboardInterrupt:
            door.cleanup()
            break
