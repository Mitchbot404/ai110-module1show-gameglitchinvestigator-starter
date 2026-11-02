# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The player tries to guess a randomly generated secret number within a limited number of attempts. The selected difficulty determines the allowed number range and attempt limit. The game provides higher/lower hints and tracks a score.
- [ ] Detail which bugs you found.
The original hints were reversed. New Game initially ignored the selected difficulty range, and the instructions showed a hardcoded range. Changing difficulty could leave an old secret active. After winning or losing, New Game could leave the game stuck in the previous end state. Attempts initially started at 1 instead of 0, and the attempts-left display lagged behind submitted guesses. The game also accepted guesses outside the selected difficulty range.
- [ ] Explain what fixes you applied.
Corrected check_guess() hint messages, used the selected low and high values when generating and displaying the active range, synchronized the secret with difficulty changes, reset status to "playing" on New Game, initialized attempts at 0, refreshed the on-screen attempt count after submissions, and rejected out-of-range guesses without reducing the remaining attempts. The secret is preserved in st.session_state across ordinary reruns.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the app with python -m streamlit run app.py and choose Easy, Normal, or Hard from the sidebar.
2. Check that the range and attempt limit match the difficulty: Easy is 1–20 with 6 attempts, Normal is 1–100 with 8 attempts, and Hard is 1–50 with 5 attempts.
3. Open Developer Debug Info to view the secret number and confirm which value the game expects.
4. Enter a number within the selected range and click Submit Guess 🚀. If the guess is too high, the game says 📉 Go LOWER!; if it is too low, the game says 📈 Go HIGHER!.
5. Confirm that each valid, incorrect guess reduces the remaining attempts by one. Try an out-of-range number to verify that an error appears and no attempt is lost.
6. Enter the secret number from Developer Debug Info to see the 🎉 Correct! message and winning result.
7. Click New Game 🔁 after winning or losing to confirm a new secret is generated and the game is playable again. Change difficulty to confirm the new game uses the newly selected range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
#python -m pytest tests/ -v

collected 14 items

tests/test_app_gameplay.py  11 passed
tests/test_game_logic.py    3 passed

======================== 14 passed in 0.40s ========================

```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
