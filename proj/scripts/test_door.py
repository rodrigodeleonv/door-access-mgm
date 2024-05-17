"""This module control the Raspberry Pi GPIO

Test open the door.
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
