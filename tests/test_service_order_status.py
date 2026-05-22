import pytest

from app.services.service_order_service import validate_status_transition
from app.utils.enums import ServiceOrderStatus

def test_open_to_in_progress_is_allowed():
    validate_status_transition(
        ServiceOrderStatus.OPEN,
        ServiceOrderStatus.IN_PROGRESS,
    )

def test_done_to_open_is_not_allowed():
    with pytest.raises(ValueError, match="Invalid status transition"):
        validate_status_transition(
            ServiceOrderStatus.DONE,
            ServiceOrderStatus.OPEN,
        )

def test_same_status_is_not_allowed():
    with pytest.raises(ValueError, match="already has this status"):
        validate_status_transition(
            ServiceOrderStatus.OPEN,
            ServiceOrderStatus.OPEN,
        )