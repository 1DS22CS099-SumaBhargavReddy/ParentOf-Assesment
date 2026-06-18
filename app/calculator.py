def calculate_accuracy_rate(fruits_sliced: int, fruits_missed: int, bombs_hit: int) -> float:
    """
    Measures the precision of fruit slicing while avoiding missed targets and bombs.
    Formula: 100 * fruits_sliced / (fruits_sliced + fruits_missed + bombs_hit)
    Returns: float in range [0.0, 100.0]
    """
    # 1. Sum up all valid target interactions (fruits sliced) and all mistakes (missed fruits and bomb hits)
    total_target = fruits_sliced + fruits_missed + bombs_hit
    
    # 2. Check for division-by-zero: if there were no valid fruit attempts or hits, return a baseline of 0.0
    if total_target == 0:
        # Return 0.0 to prevent crash and represent no accuracy rating
        return 0.0
        
    # 3. Calculate accuracy ratio, multiply by 100 to scale to 0-100, round to 4 decimal places, and cast to float
    return float(round(100.0 * fruits_sliced / total_target, 4))


def calculate_response_rate(
    fruits_sliced: int, bombs_dodged: int, max_combo: int, session_duration_seconds: int
) -> float:
    """
    Measures physical interaction speed and strategic combo efficiency.
    Formula: 0.6 * Normalized_Speed + 0.4 * Normalized_Combo
    Returns: float in range [0.0, 100.0]
    """
    # 1. Verify session duration: if duration is non-positive, set interaction speed to zero
    if session_duration_seconds <= 0:
        # Set speed to 0.0 to handle corrupt or instant-failure durations
        actions_per_second = 0.0
    else:
        # 2. Calculate the rate of correct actions (sliced + dodged) per second
        actions_per_second = (fruits_sliced + bombs_dodged) / session_duration_seconds

    # 3. Normalize speed score: scale relative to reference speed of 2.5 actions/sec, and cap at 100.0%
    speed_score = min(100.0, 100.0 * actions_per_second / 2.5)
    
    # 4. Normalize combo score: scale relative to reference max combo of 50, and cap at 100.0%
    combo_score = min(100.0, 100.0 * max_combo / 50.0)
    
    # 5. Compute the final response rate using weighted averages: 60% for speed and 40% for combo efficacy
    return float(round(0.6 * speed_score + 0.4 * combo_score, 4))


def calculate_error_rate(
    fruits_sliced: int, fruits_missed: int, bombs_hit: int, bombs_dodged: int
) -> float:
    """
    Measures the frequency and severity of player mistakes during a session.
    Formula: min(100, 100 * (fruits_missed + 3 * bombs_hit) / total_objects)
    Returns: float in range [0.0, 100.0]
    """
    # 1. Sum up all objects (fruits sliced, missed, bombs hit, dodged) to find total events
    total_objs = fruits_sliced + fruits_missed + bombs_hit + bombs_dodged
    
    # 2. Check for division-by-zero: if no objects appeared on screen, error rate is 0.0
    if total_objs == 0:
        # Return 0.0 baseline since no actions occurred
        return 0.0
        
    # 3. Calculate weighted mistakes: fruits missed count as 1, while bomb hits count as 3 due to high severity
    weighted_mistakes = fruits_missed + 3.0 * bombs_hit
    
    # 4. Divide weighted errors by total objects, scale to 100, clip the maximum to 100.0%, and round to 4 decimals
    return float(round(min(100.0, 100.0 * weighted_mistakes / total_objs), 4))


def calculate_persistence_rate(
    retries: int, session_duration_seconds: int, pause_count: int
) -> float:
    """
    Measures the player's engagement, grit, and willingness to retry despite mistakes.
    Formula: max(0, min(100, 0.5 * retries_score + 0.5 * duration_score - pause_penalty))
    Returns: float in range [0.0, 100.0]
    """
    # 1. Calculate retry score: scale user's retries (max 3) to a percentage (0-100%)
    retries_score = 100.0 * retries / 3.0
    
    # 2. Calculate duration score: scale active play duration (max 300s) to a percentage (0-100%)
    duration_score = 100.0 * session_duration_seconds / 300.0
    
    # 3. Calculate pause penalty: each pause count (max 5) subtracts up to 20 points from the score
    pause_penalty = 20.0 * pause_count / 5.0
    
    # 4. Combine score: 50% weight for retries, 50% weight for duration, minus the pause penalty
    persistence = 0.5 * retries_score + 0.5 * duration_score - pause_penalty
    
    # 5. Clip final persistence value to remain strictly within [0.0, 100.0] range and round to 4 decimals
    return float(round(max(0.0, min(100.0, persistence)), 4))


def calculate_consistency_rate(
    max_combo: int, fruits_sliced: int, error_rate: float, pause_count: int
) -> float:
    """
    Measures the stability of play flow, streak maintenance, and error avoidance.
    Formula: max(0, min(100, 0.5 * combo_consistency + 0.5 * stability - pause_penalty))
    Returns: float in range [0.0, 100.0]
    """
    # 1. Verify sliced fruit count: if zero fruits were sliced, set combo consistency score to zero
    if fruits_sliced <= 0:
        # Set consistency score to 0.0 to prevent division-by-zero
        combo_consistency = 0.0
    else:
        # 2. Calculate combo length relative to total sliced fruits, and clip at 100% to handle anomalies
        combo_consistency = min(100.0, 100.0 * max_combo / fruits_sliced)

    # 3. Calculate stability score as the inverse of the error rate (representing error avoidance)
    stability = 100.0 - error_rate
    
    # 4. Calculate pause penalty: each pause count (max 5) subtracts up to 20 points from flow consistency
    pause_penalty = 20.0 * pause_count / 5.0
    
    # 5. Combine score: 50% combo consistency, 50% stability score, minus the pause penalty
    consistency = 0.5 * combo_consistency + 0.5 * stability - pause_penalty
    
    # 6. Clip final consistency value to remain strictly within [0.0, 100.0] range and round to 4 decimals
    return float(round(max(0.0, min(100.0, consistency)), 4))


def calculate_overall_performance_score(
    accuracy_rate: float,
    response_rate: float,
    error_rate: float,
    persistence_rate: float,
    consistency_rate: float,
) -> float:
    """
    Calculates the holistic performance index combining all five cognitive rates.
    Formula: 0.3 * Accuracy + 0.25 * Response + 0.15 * (100 - Error) + 0.15 * Persistence + 0.15 * Consistency
    Returns: float in range [0.0, 100.0]
    """
    # 1. Calculate the error avoidance rate (100.0 minus error rate) so it represents positive performance
    stability = 100.0 - error_rate
    
    # 2. Apply weighted summation: Accuracy (30%), Response (25%), Stability (15%), Persistence (15%), Consistency (15%)
    overall = (
        0.30 * accuracy_rate
        + 0.25 * response_rate
        + 0.15 * stability
        + 0.15 * persistence_rate
        + 0.15 * consistency_rate
    )
    
    # 3. Clip final overall performance score to [0.0, 100.0] range and round to 4 decimals
    return float(round(max(0.0, min(100.0, overall)), 4))
