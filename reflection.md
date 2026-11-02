# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the game, the interface looked fine, but several parts of the gameplay were not working correctly. One issue was that the Higher and Lower hints were reversed, which made it confusing to find the correct number. Another problem was that the game did not always follow the selected difficulty range, especially when starting a new game. I also found problems with the attempt counter and game state, including the game not resetting properly after winning or losing.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60 when the secret is 50 | Display "Too High" and "Go LOWER!" | The original logic said "Go HIGHER!" | Incorrect hint, no Python exception |
| Select Easy mode and click New Game | Generate a secret between 1 and 20 | The original code generated numbers from 1 to 100 | No exception; `random.randint(1, 100)` ignored the difficulty |
| Click New Game after losing | Reset the status and allow another game | The previous game-over status remained active | "Game over. Start a new game to try again." |
| Start Easy mode without guessing | Display 6 attempts remaining | Originally displayed 5 because attempts initialized to 1 | Incorrect starting attempt count; no exception |


---

## 2. How did you use AI as a teammate?

I mainly used ChatGPT to help me review the code, identify bugs, suggest fixes, and create automated tests. One correct suggestion was to use the selected `low` and `high` values when generating the secret number, which I verified by switching between difficulties and checking the game. However, one suggestion was incomplete: changing the starting attempt count from 1 to 0 fixed the initial count but did not immediately update the attempts remaining after submitting a guess. I noticed this while testing the game and shared screenshots showing that the displayed number was one step behind. We then adjusted the Streamlit display using `st.empty()`, and I verified the correction by playing again and running pytest.


---

## 3. Debugging and testing your fixes

I determined whether a bug was fixed by running the game and repeating the actions that originally caused the problem. For example, I tested out-of-range guesses such as 124 in Normal mode, 65 in Easy mode, and 0 in Hard mode to confirm that the game displayed the correct error without reducing the remaining attempts. ChatGPT also helped create pytest tests for the guessing logic, difficulty ranges, attempt counting, and New Game behavior. After the changes, I ran the complete test suite in VS Code and confirmed that all 14 tests passed with no failures.


---

## 4. What did you learn about Streamlit and state?

I learned that Streamlit reruns the Python script whenever a user interacts with the application, such as clicking a button or changing a setting. This can cause problems when variables need to keep their values between interactions. Session state allows the game to remember important information, including the secret number, attempts, score, and current game status. I also learned that the order in which Streamlit displays information matters because a value can be updated correctly in the code while the screen still shows an older value.

---

## 5. Looking ahead: your developer habits

One habit I want to continue using is testing each change immediately instead of assuming that a fix works just because the code runs without errors. I also want to keep using automated tests because they help confirm that fixing one issue has not broken something else. Next time I work with AI, I would be more specific about the expected behavior and verify its suggestions before applying additional changes. This project showed me that AI-generated code can be useful, but it is not always correct or complete, so understanding and testing the code is still my responsibility.