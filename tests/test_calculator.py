from app.calculator import (
    calculate_accuracy_rate,
    calculate_response_rate,
    calculate_error_rate,
    calculate_persistence_rate,
    calculate_consistency_rate,
    calculate_overall_performance_score,
)


def test_calculate_accuracy_rate():
    # Regular case
    assert calculate_accuracy_rate(80, 10, 10) == 80.0
    # Perfect accuracy
    assert calculate_accuracy_rate(100, 0, 0) == 100.0
    # Zero targets
    assert calculate_accuracy_rate(0, 0, 0) == 0.0


def test_calculate_response_rate():
    # Under speed limit (100 actions in 100 sec = 1.0 action/sec)
    # Speed score = (1.0 / 2.5) * 100 = 40.0
    # Combo score = (20 / 50) * 100 = 40.0
    # Response = 0.6 * 40 + 0.4 * 40 = 40.0
    assert calculate_response_rate(80, 20, 20, 100) == 40.0

    # Over speed limit (200 actions in 50 sec = 4.0 action/sec)
    # Speed score capped at 100.0
    # Combo score = 100.0
    # Response = 100.0
    assert calculate_response_rate(180, 20, 50, 50) == 100.0

    # Zero duration
    assert calculate_response_rate(50, 10, 10, 0) == 8.0  # Speed is 0, combo score is 20. 0.4 * 20 = 8.0


def test_calculate_error_rate():
    # Standard case (10 missed + 3 * 2 hit = 16 errors out of 100 total objects)
    # 16% error rate
    assert calculate_error_rate(80, 10, 2, 8) == 16.0

    # Capped at 100
    # 20 missed + 3 * 10 hit = 50 errors out of 50 total objects. 50/50 = 100%
    assert calculate_error_rate(0, 20, 10, 20) == 100.0

    # Zero total objects
    assert calculate_error_rate(0, 0, 0, 0) == 0.0


def test_calculate_persistence_rate():
    # 3 retries (100%), 300s duration (100%), 0 pauses (0% penalty)
    # 0.5 * 100 + 0.5 * 100 - 0 = 100.0
    assert calculate_persistence_rate(3, 300, 0) == 100.0

    # 1 retry (33.33%), 150s (50%), 2 pauses (8% penalty)
    # Persistence = 0.5 * 33.33 + 0.5 * 50 - 8 = 16.66 + 25 - 8 = 33.6667
    assert round(calculate_persistence_rate(1, 150, 2), 2) == 33.67


def test_calculate_consistency_rate():
    # combo = 20, sliced = 80 -> combo_consistency = 25.0
    # error_rate = 20.0 -> stability = 80.0
    # pauses = 0 -> pause_penalty = 0.0
    # Consistency = 0.5 * 25 + 0.5 * 80 - 0 = 52.5
    assert calculate_consistency_rate(20, 80, 20.0, 0) == 52.5

    # Pause penalty subtraction test
    # combo = 20, sliced = 80 -> 25.0
    # stability = 80.0
    # pauses = 5 -> pause_penalty = 20.0
    # Consistency = 52.5 - 20 = 32.5
    assert calculate_consistency_rate(20, 80, 20.0, 5) == 32.5


def test_calculate_overall_performance_score():
    # All 100
    assert calculate_overall_performance_score(100.0, 100.0, 0.0, 100.0, 100.0) == 100.0
    # Normal distribution
    # 0.3 * 80 + 0.25 * 50 + 0.15 * (100 - 20) + 0.15 * 40 + 0.15 * 60
    # = 24.0 + 12.5 + 12.0 + 6.0 + 9.0 = 63.5
    assert calculate_overall_performance_score(80.0, 50.0, 20.0, 40.0, 60.0) == 63.5
