# WordHunt-Solver
This is a program for outputting all solutions in a given board from the GamePigeon game "Wordhunt".
This works pretty well to beat pretty much all normal players. 
The wordbank isn't exactly the same one that 
GamePigeon uses. It also depends how fast you can swipe


create a trie containing all possible words given our board 
- used 2019 Collins Official Scrabble Wordbank
https://boardgames.stackexchange.com/questions/38366/latest-collins-scrabble-words-list-in-text-file

DFS from each letter - > see if any path ends in a word from the wordbank
- if so, add word to a set

Sort the set by length
- print out the word, followed by its starting letter position and path in the board



To run it:
- download file.
- open on VSCode or some
- run it by pressing big green button

Or
- download
- in terminal, cd to director
- type command python3 wordhunt.py



target runtime: <1 sec

params:
- 1:20 time
- 4x4 box