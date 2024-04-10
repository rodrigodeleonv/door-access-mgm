import pytest
from django.core.exceptions import ValidationError
from datetime import time

from access_control import models


# @pytest.mark.django_db
@pytest.mark.parametrize(
    "start_time, end_time, expected",
    [
        (time(18, 0, 1), time(18, 0, 2), True),
        (time(23, 59), time(23, 59, 59), True),
        (time(0), time(0, 0, 1), True),
        (time(23), time(0), False),
        (time(6, 0), time(5, 59, 59), False),
    ],
)
def test_rfid_tag_valid_time_range_validation(start_time, end_time, expected):
    """Test for valid or invalid ranges."""
    tag = models.RFIDTag(
        tag_id="0001234567",
        owner="Owner Name",
        valid_range_start=start_time,
        valid_range_end=end_time,
        description="test",
    )
    # try:
    #     tag.clean()
    # except ValidationError:
    #     pytest.fail("ValidationError raised unexpectedly!")
    assert tag.check_valid_range() is expected


# @pytest.mark.django_db
def test_rfid_tag_clean_raises():
    tag = models.RFIDTag(
        tag_id="0001234567",
        owner="Owner Name",
        valid_range_start=time(18, 0),
        valid_range_end=time(9, 0),
    )
    with pytest.raises(ValidationError):
        tag.clean()


@pytest.mark.parametrize(
    "active, time_val, expected",
    [
        (True, time(7), True),
        (True, time(5), False),
        (False, time(7), False),
        (False, time(5), False),
    ],
)
def test_rfid_tag_check_access(active, time_val, expected):
    """Defined valid period."""
    tag = models.RFIDTag(
        tag_id="0001234567",
        owner="Owner Name",
        valid_range_start=time(6),
        valid_range_end=time(17),
        active=active,
    )
    assert tag.check_access(time_val) is expected
