
import pytest

from pet_walking_service import process_walking_routes, inspect_gps_collars


def test_invalid_routes_type_raises_value_error():
    with pytest.raises(ValueError):
        process_walking_routes(None, 5.0)


def test_negative_transport_fee_raises_value_error():
    with pytest.raises(ValueError):
        process_walking_routes([], -1.0)


def test_standard_30_walk():
    routes = [{
        "route_confirmed": True,
        "session_type": "standard_30",
        "is_weekend": False,
        "walks": [{
            "num_pets": 1,
            "aggression_alert": False,
            "needs_meds": False
        }]
    }]

    result = process_walking_routes(routes, 5.0)

    assert result["total_revenue"] == 27.0
    assert result["status"] == "COMPLETED"


def test_standard_60_walk_with_medication_and_weekend_fee():
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

    assert result["total_revenue"] == 56.0
    assert result["status"] == "COMPLETED"


def test_express_walk_with_more_than_three_pets():
    routes = [{
        "route_confirmed": True,
        "session_type": "express_15",
        "walks": [{
            "num_pets": 4,
            "aggression_alert": False,
            "needs_meds": False
        }]
    }]

    result = process_walking_routes(routes, 5.0)

    assert result["total_revenue"] == 41.4
    assert result["status"] == "COMPLETED"


def test_aggression_on_standard_30_records_incident():
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

    assert result["total_revenue"] == 6.0
    assert result["status"] == "COMPLETED"


def test_aggression_on_standard_60_stops_route():
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

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"


def test_invalid_pet_count_and_unconfirmed_route():
    routes = [
        {
            "route_confirmed": False,
            "walks": [{"num_pets": 1}]
        },
        {
            "route_confirmed": True,
            "session_type": "standard_30",
            "walks": [{
                "num_pets": 0,
                "aggression_alert": False,
                "needs_meds": False
            }]
        }
    ]

    result = process_walking_routes(routes, 5.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"


def test_unknown_session_type_triggers_audit():
    routes = [
        {"route_confirmed": True, "session_type": "unknown"}
        for _ in range(5)
    ]

    result = process_walking_routes(routes, 5.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "INCIDENT_AUDIT"


def test_empty_routes_return_zero_earnings():
    result = process_walking_routes([], 5.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_EARNINGS"


def test_empty_gps_data_returns_no_data():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_signal_recovery_returns_online():
    assert inspect_gps_collars([[10, 25, 12]]) == "ONLINE"


def test_two_consecutive_weak_gps_signals_trigger_alert():
    assert inspect_gps_collars([[10, 15, 25, 8, 9]]) == "LOST_SIGNAL_ALERT"


def test_empty_log_for_a_collar_returns_online():
    assert inspect_gps_collars([[]]) == "ONLINE"

