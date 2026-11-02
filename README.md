# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the repaired app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
The player tries to guess a randomly generated secret number within a limited number of attempts. The selected difficulty determines the allowed number range and attempt limit. The game provides higher/lower hints and tracks a score.
- [x] Detail which bugs you found.
The original hints were reversed. New Game initially ignored the selected difficulty range, and the instructions showed a hardcoded range. Changing difficulty could leave an old secret active. After winning or losing, New Game could leave the game stuck in the previous end state. Attempts initially started at 1 instead of 0, and the attempts-left display lagged behind submitted guesses. The game also accepted guesses outside the selected difficulty range.
- [x] Explain what fixes you applied.
Corrected check_guess() hint messages, used the selected low and high values when generating and displaying the active range, synchronized the secret with difficulty changes, reset status to "playing" on New Game, initialized attempts at 0, refreshed the on-screen attempt count after submissions, and rejected out-of-range guesses without reducing the remaining attempts. The secret is preserved in st.session_state across ordinary reruns.

## 📸 Demo Walkthrough

1. Start the application using `python -m streamlit run app.py` and select Easy mode, which allows 6 attempts to guess a number between 1 and 20.
2. Open Developer Debug Info to view the secret number. For this example, assume the secret is 15.
3. Enter 10 and click Submit Guess. The game displays "📈 Go HIGHER!" and reduces the remaining attempts to 5.
4. Enter 18. The game displays "📉 Go LOWER!" and reduces the remaining attempts to 4.
5. Enter 15. The game displays "🎉 Correct!" and announces the win.
6. Start a new game using New Game. The game generates another secret, resets the attempts, and allows the player to continue.
7. Switch to Normal or Hard mode to confirm that the game adjusts its range and attempt limit.




## 🧪 Test Results

```text
============================== test session starts ============================
platform win32 -- Python 3.14.2, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\mitch\AppData\Local\Python\pythoncore-3.14-64\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\mitch\OneDrive\Documents\ChatGPT\School\Game Glitch Investigator\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.16.0
collected 14 items                                                                     

tests/test_app_gameplay.py::test_out_of_range_guess_does_not_use_attempt[Easy-65] PASSED [  7%]
tests/test_app_gameplay.py::test_out_of_range_guess_does_not_use_attempt[Normal-124] PASSED [ 14%]
tests/test_app_gameplay.py::test_out_of_range_guess_does_not_use_attempt[Hard-0] PASSED [ 21%]
tests/test_app_gameplay.py::test_valid_guesses_count_from_zero_and_end_on_last_attempt[Easy] PASSED [ 28%]
tests/test_app_gameplay.py::test_valid_guesses_count_from_zero_and_end_on_last_attempt[Normal] PASSED [ 35%]
tests/test_app_gameplay.py::test_valid_guesses_count_from_zero_and_end_on_last_attempt[Hard] PASSED [ 42%]
tests/test_app_gameplay.py::test_new_game_resets_status_and_is_playable[won] PASSED [ 50%]
tests/test_app_gameplay.py::test_new_game_resets_status_and_is_playable[lost] PASSED [ 57%]
tests/test_app_gameplay.py::test_difficulty_change_starts_game_in_selected_range[Easy] PASSED [ 64%]
tests/test_app_gameplay.py::test_difficulty_change_starts_game_in_selected_range[Normal] PASSED [ 71%]
tests/test_app_gameplay.py::test_difficulty_change_starts_game_in_selected_range[Hard] PASSED [ 78%]
tests/test_game_logic.py::test_winning_guess PASSED                              [ 85%]
tests/test_game_logic.py::test_guess_too_high PASSED                             [ 92%]
tests/test_game_logic.py::test_guess_too_low PASSED                              [100%]

============================== 14 passed in 0.36s =============================
```

## 🚀 Stretch Features

Not attempted. Focused on fixing the original gameplay bugs, refactoring the code, and verifying the repairs through automated tests.