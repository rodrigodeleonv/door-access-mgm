"""Define the access control management script."""

import logging

from django.utils import timezone
from django.conf import settings

from access_control import models
from scripts.rpi_gpio import open_door

logger = logging.getLogger(__name__)


def access_validation(tag: models.RFIDTag) -> bool:
    """Verify is the Tag ID is valid and if so, open the door.

    Args:
        tag: RFIDTag model

    Returns:
        True for valid Tag ID and correct period of time, etc. False otherwise.
    """
    current_time = timezone.now().time()
    can_access = tag.check_access(current_time)
    # print(f"can_access={can_access}")
    if can_access:
        logger.info(f"Allowing access to Tag ID: {tag.tag_id}")
        open_door(settings.RPI_GPIO_PIN_OPEN, settings.RPI_TIME_SIGNAL_OPEN)
    else:
        logger.info(f"Denying access to Tag ID: {tag.tag_id}")
    return can_access
