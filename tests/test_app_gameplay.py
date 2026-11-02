"""Focused gameplay regression tests for the Streamlit app."""

import random
import runpy
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import logic_utils


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}
RANGES = {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 50)}


class SessionState(dict):
    """Support Streamlit-style attribute and dictionary access."""

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc

    def __setattr__(self, key, value):
        self[key] = value


class Rerun(Exception):
    pass


class Stop(Exception):
    pass


@pytest.fixture
def run_game(monkeypatch):
    # Keep these tests focused on app.py. check_guess() has its own unit tests.
    def check_guess(guess, secret):
        if guess == secret:
            return "Win", "🎉 Correct!"
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"

    monkeypatch.setattr(logic_utils, "check_guess", check_guess)

    def run(*, difficulty="Easy", guess="", button=None, state=None):
        state = state if state is not None else SessionState()
        st = MagicMock()
        st.session_state = state
        st.sidebar.selectbox.return_value = difficulty
        st.text_input.return_value = guess
        st.button.side_effect = lambda label: label.startswith(button) if button else False
        st.checkbox.return_value = True
        st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        st.rerun.side_effect = Rerun
        st.stop.side_effect = Stop
        monkeypatch.setitem(sys.modules, "streamlit", st)

        try:
            runpy.run_path(str(APP_PATH), run_name="__main__")
        except (Rerun, Stop):
            pass
        return st, state

    return run


@pytest.mark.parametrize(
    "difficulty,invalid_guess",
    [("Easy", "65"), ("Normal", "124"), ("Hard", "0")],
)
def test_out_of_range_guess_does_not_use_attempt(run_game, difficulty, invalid_guess):
    state = SessionState(secret=10, attempts=0, score=0, status="playing",
                         history=[], active_difficulty=difficulty)
    st, state = run_game(difficulty=difficulty, guess=invalid_guess,
                         button="Submit Guess", state=state)

    low, high = RANGES[difficulty]
    st.error.assert_called_once_with(f"Please enter a number between {low} and {high}.")
    assert state.attempts == 0
    assert state.score == 0
    assert state.history == []
    assert f"Attempts left: {LIMITS[difficulty]}" in st.empty.return_value.info.call_args.args[0]


@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_valid_guesses_count_from_zero_and_end_on_last_attempt(run_game, difficulty):
    state = SessionState(secret=10, attempts=0, score=0, status="playing",
                         history=[], active_difficulty=difficulty)
    limit = LIMITS[difficulty]

    st, state = run_game(difficulty=difficulty, state=state)
    assert state.attempts == 0
    assert f"Attempts left: {limit}" in st.empty.return_value.info.call_args.args[0]

    for attempt in range(1, limit + 1):
        st, state = run_game(difficulty=difficulty, guess="1",
                             button="Submit Guess", state=state)
        assert state.attempts == attempt
        assert f"Attempts left: {limit - attempt}" in st.empty.return_value.info.call_args.args[0]
        assert state.status == ("lost" if attempt == limit else "playing")

    assert any("Out of attempts!" in call.args[0] for call in st.error.call_args_list)


@pytest.mark.parametrize("previous_status", ["won", "lost"])
def test_new_game_resets_status_and_is_playable(run_game, monkeypatch, previous_status):
    state = SessionState(secret=10, attempts=6, score=25, status=previous_status,
                         history=[2, 5], active_difficulty="Easy")
    calls = []

    def randint(low, high):
        calls.append((low, high))
        return 10

    monkeypatch.setattr(random, "randint", randint)
    st, state = run_game(difficulty="Easy", button="New Game", state=state)

    st.rerun.assert_called_once()
    assert calls == [(1, 20)]
    assert state.secret == 10
    assert state.attempts == 0
    assert state.status == "playing"
    assert state.score == 25  # New Game must not change existing scoring behavior.
    assert state.history == [2, 5]

    st, state = run_game(difficulty="Easy", guess="1",
                         button="Submit Guess", state=state)
    assert state.attempts == 1
    assert state.status == "playing"
    st.stop.assert_not_called()


@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_difficulty_change_starts_game_in_selected_range(run_game, monkeypatch, difficulty):
    state = SessionState(secret=90, attempts=4, score=7, status="lost",
                         history=[2], active_difficulty="Other")
    calls = []

    def randint(low, high):
        calls.append((low, high))
        return low

    monkeypatch.setattr(random, "randint", randint)
    st, state = run_game(difficulty=difficulty, state=state)

    assert calls == [RANGES[difficulty]]
    assert state.secret == RANGES[difficulty][0]
    assert state.attempts == 0
    assert state.status == "playing"
    assert state.active_difficulty == difficulty
    assert f"Attempts left: {LIMITS[difficulty]}" in st.empty.return_value.info.call_args.args[0]
