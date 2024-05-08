"""Provisioning script.

.. code-block:: bash

   python proj/manage.py runscript provision
"""

import json
import logging

from decouple import config
from rest_framework.authtoken.models import Token

from users.models import User
from access_control.models import RFIDTag

logger = logging.getLogger(__name__)


def provision_superuser() -> None:
    """Provision Superuser if not exists."""
    exists_superuser = User.objects.filter(is_superuser=True).exists()
    if not exists_superuser:
        logger.info("Creating superuser")
        username = config("PROVISION_SUPERUSER_EMAIL")
        password = config("PROVISION_SUPERUSER_PASSWORD")
        super_u = User.objects.create_superuser(
            email=username, password=password, first_name="Super", last_name="User"
        )
        # Create token for superuser
        Token.objects.create(user=super_u)
    else:
        logger.info("Do not create superuser, already exists")


def provison_tags() -> None:
    """Provision Tags from JSON file."""
    logger.info("Provision RFID Tags")
    sup = User.objects.filter(is_superuser=True).first()
    with open("provision/tags.json") as f:
        tags = json.load(f)
    for tag in tags["tags"]:
        tag_id = tag["tag_id"].strip()
        description = tag["description"].strip()

        if not RFIDTag.objects.filter(tag_id=tag_id).exists():
            RFIDTag.objects.create(
                tag_id=tag_id, description=description, created_by=sup
            )
            logger.info(f"Tag {tag_id} created")


def run():
    try:
        provision_superuser()
    except Exception:
        logger.exception("Provision superuser failed")
    try:
        provison_tags()
    except Exception:
        logger.exception("Provision tags failed")
