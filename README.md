# Wordle-Solver

Wordle Solver is a script tool that solves Wordle puzzles. Users can input their word guesses as they work to solve their puzzle, and the tool will provide optimized solution possibilities. 

## How does it work?

The tool analyzes the Wordle word bank to find the most commonly used letters within each placement of a five-letter word. It calculates a "score" by breaking down the order that the letters appear in a word and compares it to the overall frequency those letters appear in that same placement throughout the word bank. The tool provides the word, or words, with the highest score as its output.

For example, let's look at the word "SCARE". The tool breaks down each letter of the word, in order, and compares it to how many times those letters appear in that same placement when compared to all possible word choices. Frequencies for "SCARE" would be measured like this:

"S" = 366
"C" = 40
"A" = 307
"R" = 152
"E" = 424

What this means is that the letter "S" shows up 366 times out of all the words in the word bank when it is used as the first letter. The letter "C" occurs 40 times when it is the second letter, and so-on. The score is then calculated as an aggregation of these frequencies:
366 + 40 + 307 + 152 + 424 = 1289

The tool provides word options with the highest score. Once the user feeds their guess into Wordle, they can return to the tool and input which letters are either: correct and in the right order (green), correct but not in the right order (yellow), or not in the word (grey). Once input from the user is received, the tool eliminates words that do not match the given criteria and the remaining word bank is re-analyzed to find remaining options with the highest score.

## How do I use the tool?

Run the program on Python 3.10.4+ and follow along with the prompts. Note that when entering letters while working to solve your word, the tool will remember prior entries. For example: if you enter the letter "A" as a grey letter after your first attempt, you do not need to re-enter it on or after your second attempt. Starting a new Wordle with the tool open will reset past entries. 
