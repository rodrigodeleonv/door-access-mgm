"""Define the access control management script."""

import logging

from django.utils import timezone

from access_control import models
from access_control.rpi_gpio_conf import get_door

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
    if can_access:
        logger.info(f"Allowing access to Tag ID: {tag.tag_id}")
        door = get_door()
        door.open_door()
    else:
        logger.info(f"Denying access to Tag ID: {tag.tag_id}")
    return can_access
