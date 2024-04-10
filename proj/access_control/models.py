from datetime import time
import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class BaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class RFIDTag(BaseModel):
    """The Tag or Card in RFID context.

    Save all the Tags you want to allow to give access.
    """

    # class Meta:
    #     indexes = [models.Index(fields=["owner"])]

    created_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="created_tags"
    )
    tag_id = models.CharField(max_length=20, primary_key=True)
    owner = models.CharField(_("owner"), max_length=150)
    description = models.TextField(default="", blank=True)

    # Validations fields
    valid_range_start = models.TimeField(default="00:00")
    valid_range_end = models.TimeField(default="23:59:59")
    active = models.BooleanField(default=True, help_text="The Tag (card) is active")

    def check_access(self, time_value: time) -> bool:
        """When the Tag ID is found. Verify for permissions.

        |                   .                   |       .
        Start          valid time              end      invalid

        Args:
            time_value: value to compare with the range valid_range_start to valid_range_end.
                Usually time_value must be the current time or timezone.now().time()

        Returns:
            True for valid Tag ID and correct period of time, False otherwise.
        """
        check = self.active and (
            self.valid_range_start <= time_value <= self.valid_range_end
        )
        logger.debug(f"RFID Tag is valid={check}")
        return check

    def check_valid_range(self) -> bool:
        return self.valid_range_start < self.valid_range_end

    def clean(self):
        """Method to perform model-level validation."""
        if not self.check_valid_range():
            raise ValidationError(
                {
                    "valid_range_start": ValidationError(
                        _("valid_range_start must be before valid_range_end.")
                    ),
                    "valid_range_end": ValidationError(
                        _("valid_range_end must be after valid_range_start.")
                    ),
                }
            )

    def __str__(self) -> str:
        return f"{self.tag_id}"


class LogTag(models.Model):
    """Audit or log the event when the card is used"""

    rfid_tag = models.ForeignKey(
        RFIDTag, on_delete=models.CASCADE, related_name="rfid_tags"
    )
    access_date = models.DateTimeField(default=timezone.now)
    allowed = models.BooleanField()
