import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "hint" not in st.session_state:
    st.session_state.hint = None

if "error" not in st.session_state:
    st.session_state.error = None

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.hint = None
    st.session_state.error = None

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if st.session_state.hint and st.session_state.status == "playing":
    st.warning(st.session_state.hint)
if st.session_state.error:
    st.error(st.session_state.error)

if new_game:
    st.session_state.attempts = 0
    """
    Fix: Made sure the secret number is within the range of difficulty level using agent mode.
    """
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.hint = None
    st.session_state.error = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}. Start a new game to play again."
        )
    else:
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            "Start a new game to try again."
        )
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.hint = None
        st.session_state.error = err
        st.rerun()
    else:
        st.session_state.error = None
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        st.session_state.hint = message if show_hint else None

        st.session_state.score = update_score(
            attempt_number=st.session_state.attempts,
            attempt_limit=attempt_limit,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.hint = None
            st.rerun()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.session_state.score = 0
                st.session_state.hint = None
                st.rerun()
            else:
                st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
