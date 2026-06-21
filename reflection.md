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
|60|Hint: "GO LOWER!"|Hint: "GO HIGHER!"|None|    
|Chose "Easy" difficulty.|"Guess a number between 1 and 20." and the secret number to be in range.|"Guess a number between 1 and 100." and the secret number was out of range.|None|
|Pressed the "New Game" button.|Game to restart and allow me to input guesses.|Game never restarted and I was not allowed to input guesses.|None|
|Input a guess.|"Attempts left: 1"|"Attempts left: 0"|None| 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code on this project and one example of an AI suggestion that was correct was when it told me that the hints were reversed and it told me 
what lines to fix. This was a simple fix but something that could have easily been overlooked and to check I tried the program in the browser and it 
worked correctly. An example of an AI suggestion that was misleading and incorrect was when I wanted to make it possible for the number of attempts to 
update when clicking the submit guess button instead of when you press enter to input the next guess. It suggested to change the placement of the 
buttons, which did not do anything. To fix this I had to reverse the action and then explain in more detail what I wanted to change. This resulted in correct changes that I check by using the program in browser.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

To decide wether a bug was really fixed I tested it out by using the program in the browser. An example of this is when I 
was fixing the logic for the hints and the first fix did not work as expected because when I was inputting the number 100 
as a guess it told me to go higer and then I did it again for a second time and it told me to go lower. I explained the bug 
to the ai agent and it suggested to take out a line that converted numbers to strings if it was a even number attempt. I 
accpeted the change and tried it in the browser and it worked as expected.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
