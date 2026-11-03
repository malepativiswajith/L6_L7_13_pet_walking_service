
import pytest

from pet_walking_service import (
    process_walking_routes,
    inspect_gps_collars
)


def test_invalid_routes_argument():
    with pytest.raises(ValueError):
        process_walking_routes(None, 5.0)


def test_negative_transport_fee():
    with pytest.raises(ValueError):
        process_walking_routes([], -1.0)


def test_empty_routes_list():
    result = process_walking_routes([], 5.0)
    assert result == {
        "total_revenue": 0.0,
        "status": "ZERO_EARNINGS"
    }


def test_unconfirmed_route_and_default_session():
    routes = [
        {
            "route_confirmed": False,
            "session_type": "standard_60",
            "walks": [{"num_pets": 2}]
        },
        {
            "route_confirmed": True,
            "walks": [{"num_pets": 1}]
        }
    ]

    result = process_walking_routes(routes, 5.0)

    assert result == {
        "total_revenue": 27.0,
        "status": "COMPLETED"
    }


def test_standard_60_with_medication_and_weekend_fee():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_60",
        "is_weekend": True,
        "walks": [{
            "num_pets": 2,
            "aggression_alert": False,
            "needs_meds": True
        }]
    }]

    result = process_walking_routes(routes, 5.0)

    assert result == {
        "total_revenue": 56.0,
        "status": "COMPLETED"
    }


def test_express_session_discount():
    routes = [{
        "route_confirmed": True,
        "session_type": "express_15",
        "walks": [{"num_pets": 4}]
    }]

    result = process_walking_routes(routes, 5.0)

    assert result == {
        "total_revenue": 41.4,
        "status": "COMPLETED"
    }


def test_invalid_session_type():
    routes = [{
        "route_confirmed": True,
        "session_type": "premium"
    }]

    result = process_walking_routes(routes, 5.0)

    assert result["status"] == "ZERO_EARNINGS"


def test_more_than_four_invalid_sessions_trigger_audit():
    routes = [
        {"route_confirmed": True, "session_type": "invalid"}
        for _ in range(5)
    ]

    result = process_walking_routes(routes, 5.0)

    assert result == {
        "total_revenue": 0.0,
        "status": "INCIDENT_AUDIT"
    }


def test_zero_pet_count():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_30",
        "walks": [{"num_pets": 0}]
    }]

    result = process_walking_routes(routes, 5.0)

    assert result["status"] == "ZERO_EARNINGS"


def test_aggression_on_standard_30_with_medication():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_30",
        "walks": [{
            "num_pets": 1,
            "aggression_alert": True,
            "needs_meds": True
        }]
    }]

    result = process_walking_routes(routes, 5.0)

    assert result == {
        "total_revenue": 6.0,
        "status": "COMPLETED"
    }


def test_aggression_on_standard_60_stops_walk():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_60",
        "walks": [{
            "num_pets": 1,
            "aggression_alert": True,
            "needs_meds": True
        }]
    }]

    result = process_walking_routes(routes, 5.0)

    assert result == {
        "total_revenue": 0.0,
        "status": "ZERO_EARNINGS"
    }


def test_weekend_route_without_walks():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_30",
        "is_weekend": True,
        "walks": []
    }]

    result = process_walking_routes(routes, 5.0)

    assert result == {
        "total_revenue": 5.0,
        "status": "COMPLETED"
    }


def test_empty_gps_matrix():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_signal_recovery_and_threshold_boundary():
    assert inspect_gps_collars([[], [10, 20, 19]]) == "ONLINE"


def test_two_consecutive_weak_gps_signals():
    assert inspect_gps_collars([[10, 19]]) == "LOST_SIGNAL_ALERT"
