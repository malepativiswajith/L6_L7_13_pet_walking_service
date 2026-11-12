
import pytest
from hypothesis import given, strategies as st

from processor import (
    parse_walk_schedule,
    compute_pace_per_pet,
    lookup_temperament_surcharge
)


# Fuzz testing: parse_walk_schedule
@given(st.text() | st.none())
def test_parse_walk_schedule_no_crash(s):
    try:
        parse_walk_schedule(s)
    except Exception as e:
        pytest.fail(
            f"parse_walk_schedule crashed with input {s!r}: "
            f"{type(e).__name__}: {e}"
        )


# Fuzz testing: compute_pace_per_pet
@given(st.text() | st.none())
def test_compute_pace_per_pet_safe(s):
    try:
        compute_pace_per_pet(s)
    except Exception as e:
        pytest.fail(
            f"compute_pace_per_pet crashed with input {s!r}: "
            f"{type(e).__name__}: {e}"
        )


# Fuzz testing: lookup_temperament_surcharge
@given(st.text() | st.none())
def test_lookup_temperament_surcharge_safe(s):
    try:
        lookup_temperament_surcharge(s)
    except Exception as e:
        pytest.fail(
            f"lookup_temperament_surcharge crashed with input {s!r}: "
            f"{type(e).__name__}: {e}"
        )
