# Words of Wonders: Fugo Games
Automate game using `Python`

## How it works.
1. `Capture the Game Screen`: I used PyAutoGUI to take screenshots of the game board.

![alt text](./examples/screenshot.png)

2. `OCR Letter Recognition`: With EasyOCR, I extracted the letters from the game wheel to figure out the available ones.

![alt text](./examples/letters.png)

3. `Word Prediction`: I utilized a huge dictionary of over 400k words (found on GitHub as words.txt) to predict the possible valid words that could be formed from the letters.
4. `Automating Gameplay`: The system then uses PyAutoGUI to drag and drop the letters onto the game board to form the words and advance in the game.

## Demo
https://raw.githubusercontent.com/krishsharma0413/words-of-wonders/refs/heads/main/examples/example%20video.mp4