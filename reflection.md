# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first glitch that I found was that the range did not change with the difficulty 
because when switching from Normal to Easy, the range was still 1-100 instead of 
1-20, and the game was letting me input guesses higher or lower than the actual 
range. The second glitch that I found was with the hints, as when I inputted a 
guess that was higher than the secret number, I was told to go even higher. The 
third glitch is that when pressing the New Game button when finishing a session, 
the game never restarts and keeps saying game over. The fourth glitch is that the 
number of attempts is wrong because when the difficulty level is hard the game 
gives the player 5 attempts, I was only allowed 4.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|   60  |    "Go LOWER!"    |   "GO HIGHER!"  |          None          |
|-------|-------------------|-----------------|------------------------|
| | | | |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
