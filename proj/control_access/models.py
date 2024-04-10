from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class RFIDTag(BaseModel):
    """The Tag or Card in RFID context."""

    class Meta:
        indexes = [models.Index(fields=["owner"])]

    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="created_tags")
    tag_id = models.CharField(max_length=20, primary_key=True)
    owner = models.CharField(_("owner"), max_length=150)
    description = models.TextField()
    start = models.TimeField
    end = models.TimeField
    active = models.BooleanField(default=True)

    def has_access(self) -> bool:
        """When the Tag ID is found. Verify for permissions."""
        # Verify date and time
        # return self.active and

    def __str__(self) -> str:
        return f"{self.tag_id}"
