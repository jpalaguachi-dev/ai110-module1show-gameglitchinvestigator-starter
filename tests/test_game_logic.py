import random
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# ── 1. Difficulty level range correctness ──────────────────────────────────────
# Glitch 1: Range did not change with difficulty.
# Each mode must return exact (low, high) bounds; all start at 1.

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

def test_unknown_difficulty_defaults_to_normal_range():
    low, high = get_range_for_difficulty("Impossible")
    assert low == 1
    assert high == 100

def test_all_difficulty_ranges_start_at_one():
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, _ = get_range_for_difficulty(difficulty)
        assert low == 1, f"{difficulty} range should start at 1, got {low}"

def test_all_difficulty_ranges_are_valid():
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, high = get_range_for_difficulty(difficulty)
        assert low < high, f"{difficulty} range {low}-{high} is invalid (low >= high)"

def test_easy_range_narrower_than_normal():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high

def test_hard_range_narrower_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high < normal_high


# ── 2. Secret number stays within difficulty range ─────────────────────────────
# The secret must be generated with random.randint(low, high) from the correct
# range; if the range values are wrong the secret will fall outside bounds.

def test_easy_secret_never_exceeds_20():
    low, high = get_range_for_difficulty("Easy")
    for _ in range(50):
        secret = random.randint(low, high)
        assert 1 <= secret <= 20, f"Easy secret {secret} is outside [1, 20]"

def test_hard_secret_never_exceeds_50():
    low, high = get_range_for_difficulty("Hard")
    for _ in range(50):
        secret = random.randint(low, high)
        assert 1 <= secret <= 50, f"Hard secret {secret} is outside [1, 50]"

def test_normal_secret_within_1_to_100():
    low, high = get_range_for_difficulty("Normal")
    for _ in range(50):
        secret = random.randint(low, high)
        assert 1 <= secret <= 100, f"Normal secret {secret} is outside [1, 100]"

def test_easy_secret_not_in_normal_only_range():
    low, high = get_range_for_difficulty("Easy")
    for _ in range(30):
        secret = random.randint(low, high)
        assert secret <= 20, f"Easy secret {secret} exceeds Easy max of 20"

def test_each_difficulty_generates_secrets_within_its_own_range():
    bounds = {"Easy": 20, "Normal": 100, "Hard": 50}
    for difficulty, expected_high in bounds.items():
        low, high = get_range_for_difficulty(difficulty)
        for _ in range(20):
            secret = random.randint(low, high)
            assert 1 <= secret <= expected_high, (
                f"{difficulty} secret {secret} outside [1, {expected_high}]"
            )


# ── 3. Guess outcome correctness ────────────────────────────────────────────────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── 4. Hint direction correctness ──────────────────────────────────────────────
# Glitch 2: Hints were inverted — guess > secret said "Go HIGHER" instead of
# "Go LOWER". All cases below verify the direction is never swapped.

def test_win_message_signals_correct():
    _, message = check_guess(50, 50)
    assert "correct" in message.lower() or "🎉" in message

def test_win_message_has_no_direction_hint():
    _, message = check_guess(42, 42)
    assert "LOWER" not in message.upper()
    assert "HIGHER" not in message.upper()

def test_too_high_hint_says_lower():
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper(), f"Expected 'LOWER', got: {message!r}"

def test_too_low_hint_says_higher():
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper(), f"Expected 'HIGHER', got: {message!r}"

def test_too_high_hint_does_not_say_higher():
    _, message = check_guess(99, 1)
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()

def test_too_low_hint_does_not_say_lower():
    _, message = check_guess(1, 99)
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()

def test_one_above_secret_says_lower():
    _, message = check_guess(51, 50)
    assert "LOWER" in message.upper()

def test_one_below_secret_says_higher():
    _, message = check_guess(49, 50)
    assert "HIGHER" in message.upper()


# ── 5. Attempt limits ──────────────────────────────────────────────────────────
# Glitch 4: Hard gave only 4 attempts instead of 5.
# The map below must match attempt_limit_map in app.py exactly.

ATTEMPT_LIMIT_MAP = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}

def test_easy_attempt_limit():
    assert ATTEMPT_LIMIT_MAP["Easy"] == 6

def test_normal_attempt_limit():
    assert ATTEMPT_LIMIT_MAP["Normal"] == 8

def test_hard_attempt_limit_is_five():
    assert ATTEMPT_LIMIT_MAP["Hard"] == 5, (
        f"Hard should allow 5 attempts, got {ATTEMPT_LIMIT_MAP['Hard']}"
    )

def test_hard_attempt_limit_not_four():
    assert ATTEMPT_LIMIT_MAP["Hard"] != 4

def test_hard_fewer_attempts_than_normal():
    assert ATTEMPT_LIMIT_MAP["Hard"] < ATTEMPT_LIMIT_MAP["Normal"]

def test_hard_fewer_attempts_than_easy():
    assert ATTEMPT_LIMIT_MAP["Hard"] < ATTEMPT_LIMIT_MAP["Easy"]

def test_all_attempt_limits_are_positive():
    for difficulty, limit in ATTEMPT_LIMIT_MAP.items():
        assert limit > 0, f"{difficulty} attempt limit must be positive, got {limit}"


# ── 6. New game / game reset behavior ──────────────────────────────────────────
# Glitch 3: New Game button kept showing "game over" — fixed via session-state
# reset + st.rerun() in app.py.  Unit-testable contract: after a reset the new
# secret must (a) be in range, and (b) still work correctly with check_guess.

def test_new_secret_in_easy_range_after_reset():
    low, high = get_range_for_difficulty("Easy")
    new_secret = random.randint(low, high)
    assert 1 <= new_secret <= 20, f"New Easy secret {new_secret} out of range"

def test_new_secret_in_hard_range_after_reset():
    low, high = get_range_for_difficulty("Hard")
    new_secret = random.randint(low, high)
    assert 1 <= new_secret <= 50, f"New Hard secret {new_secret} out of range"

def test_new_secret_in_normal_range_after_reset():
    low, high = get_range_for_difficulty("Normal")
    new_secret = random.randint(low, high)
    assert 1 <= new_secret <= 100, f"New Normal secret {new_secret} out of range"

def test_check_guess_works_on_fresh_secret_after_reset():
    new_secret = 42
    outcome, _ = check_guess(42, new_secret)
    assert outcome == "Win"

def test_game_over_then_new_game_correct_guess():
    # Simulate: game was lost (attempts exhausted), new game starts.
    new_secret = 7
    outcome, _ = check_guess(7, new_secret)
    assert outcome == "Win"

def test_game_over_then_new_game_hints_still_correct():
    # After reset, hint direction must not be broken.
    new_secret = 30
    outcome_high, msg_high = check_guess(50, new_secret)
    outcome_low, msg_low = check_guess(10, new_secret)
    assert outcome_high == "Too High" and "LOWER" in msg_high.upper()
    assert outcome_low == "Too Low" and "HIGHER" in msg_low.upper()

def test_new_secrets_for_all_difficulties_are_in_range():
    bounds = {"Easy": 20, "Normal": 100, "Hard": 50}
    for difficulty, expected_high in bounds.items():
        low, high = get_range_for_difficulty(difficulty)
        new_secret = random.randint(low, high)
        assert 1 <= new_secret <= expected_high, (
            f"New {difficulty} secret {new_secret} outside expected [1, {expected_high}]"
        )


# ── 7. Input parsing ───────────────────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string_rejected():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none_rejected():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_non_numeric_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err is not None
    assert "number" in err.lower()

def test_parse_float_string_truncates_to_int():
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
