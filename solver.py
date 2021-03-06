from collections import Counter
from operator import index
from turtle import update
from time import sleep

# .txt file contains all possible answers generated by wordle
wordle_file = open('answers.txt')

wordle_words = wordle_file.read().splitlines()

# .txt file contains letters 'a'-'z' of the english alphabet
alphabet_file = open('alphabet.txt')

alphabet_list = alphabet_file.read().splitlines()

# convert alphabet list to dictionary ...
# this will be used to track counts of
# letter occurrences in words ...
# example output: { a : 0, b : 0, and so on }
def convert(alphabet):
    letter_tracker_dictionary = {
        letter: 0 for letter in alphabet
    }

    return letter_tracker_dictionary


# creates a list of tuples
# which tracks how many times each letter of the alphabet
# is used as the index of each word ...
# example output, using string_index = 0 as argument:
# [('s', 366), ('c', 198) ...]
def count_letters_in_index(string_index, word_list):

    # { a : 0, b : 0, etc. }
    letter_tracker = convert(alphabet_list)

    letters = []

    for word in word_list:
        letters.append(word[string_index])

    for key, value in letter_tracker.items():
        letter_tracker[key] = letters.count(key)
    
    counter = Counter(letter_tracker)

    ordered_by_most_common = counter.most_common(26)

    return ordered_by_most_common


# run prior function for all indices 
# of a 5-letter word ...
# example output:
# [ [('s', 366), ('c', 198) ...],
# [('a', 304), ('o', 279) ...],
# [('a', 307), ('i', 266) ...],
# [('e', 318), ('n', 182) ...],
# [('e', 424), ('y', 364) ...] ]
def count_all_letters(word_list):

    list = []

    for i in range(0, 5):
        list.append(count_letters_in_index(i, word_list))

    return list


# gives a score to a word based on how many
# words share a letter in that same index ...
# a higher score means more words use that letter ...
# Example: for the word 'scare'
# s = 366, c = 40, a = 307, r = 152, e = 424
# 366 + 40 + 307 + 152 + 424 = 1289
# therefore, 'scare' has a word score of 1289
def get_word_score(single_word, letter_score_values):

    word_score = 0

    index_counter = 0

    while index_counter < 5:

        for tuple in letter_score_values[index_counter]:

            # if letter in tuple matches letter of index counter... 
            if tuple[0] == single_word[index_counter]:
                # take letter count in tuple and add it to word score 
                word_score += tuple[1]

        index_counter += 1
    
    return word_score


def assign_word_scores(word_list):

    word_scores = {
        word : 0 for word in word_list
        }

    letter_score_table = count_all_letters(word_list)

    for key in word_scores:
        this_score = get_word_score(key, letter_score_table)
        word_scores[key] = this_score

    return word_scores


def get_word_choices(word_list=wordle_words):
    
    word_scores = assign_word_scores(word_list)

    highest_score = max(word_scores.values())

    best_choices = [ key for key in word_scores if word_scores[key] == highest_score ] 

    return best_choices
    

def get_green_letters():

    one_thru_five = [ number for number in range(1, 6) ]

    green_letters = {}

    for number in one_thru_five:
        user_input = input(f'Enter the green letter in position {number}. If there is none, hit enter: ')
    
        if user_input.lower() == '':
            # subtracting 1 from number to store the index in dictionary
            green_letters.update({number - 1 : ''})
        elif user_input.lower() not in alphabet_list:
            print(f'The green letter in position {number} is not a valid letter. \nInput will be ignored.')
            green_letters.update({number - 1 : ''})
        else:
            green_letters.update({number - 1 : user_input.lower()})

    return green_letters


def get_yellow_letters():

    one_thru_five = [ number for number in range(1, 6) ]

    yellow_letters = {}

    for number in one_thru_five:
        user_input = input(f'Enter the yellow letter in position {number}. If there is none, hit enter: ')
    
        if user_input.lower() == '':
            # subtracting 1 from number to store the index in dictionary
            yellow_letters.update({number - 1 : ''})
        elif user_input.lower() not in alphabet_list:
            print(f'The yellow letter in position {number} is not a valid letter. \nInput will be ignored.')
            yellow_letters.update({number - 1 : ''})
        else:
            yellow_letters.update({number - 1 : user_input.lower()})

    return yellow_letters


def get_grey_letters():

    grey_letters = []

    loop = True

    while loop:

        user_input = input("Enter a grey letter and hit enter. \nIf there are no more grey letters, hit enter: ")

        if user_input == '':
            break
        if user_input.lower() not in alphabet_list:
            print('The grey letter is not a valid letter. \nInput will be ignored.')
            pass
        # in case user tries to add the same letter more than once, ignore.
        if user_input.lower() in grey_letters:
            print(f"'{user_input.upper()}' has already been added.")
            pass
        else: 
            grey_letters.append(user_input.lower())

    return grey_letters


def update_word_list_with_green_letters(word_list):

    updated_word_list = []

    green_letters = get_green_letters()

    if len(green_letters) == 0:
        return word_list
    else:
        for word in word_list:

            # assume the word should be added to the new word list.
            word_meets_green_requirements = True

            index = 0

            while index in range(0, 5):
                # if there is no green letter available for an index, skip.
                if green_letters[index] == '':
                    pass
                # if the word doesn't have the green letter in that index, it should not be added.
                elif green_letters[index] != word[index]:
                    word_meets_green_requirements = False
                    break

                index += 1 
            
            # if the word still meets requirements, add it to the new list.
            if word_meets_green_requirements:
                updated_word_list.append(word)

        # converting green_letters from dict to list for later use 
        green_letters_list = []

        for index, letter in green_letters.items():
            if letter != '':
                green_letters_list.append(letter)

        return updated_word_list, green_letters_list


def update_word_list_with_yellow_letters(word_list):

    updated_word_list = []

    yellow_letters = get_yellow_letters()

    if len(yellow_letters) == 0:
        return word_list
    else: 

        # this list will be used to check that all yellow letters
        # are somewhere in the word
        # ex: for a letter bank of ['e','l','l'] ... 
        # 'hello' could be a valid word that gets added.
        letters_only = []

        for index, letter in yellow_letters.items():
            if letter != '':
                letters_only.append(letter)
        
        for word in word_list: 
            
            index = 0

            # assume the word should be added to the new word list.
            yellow_letter_index_is_not_word_index = True
            all_yellow_letters_are_in_word = True

            # first: words that have the yellow letter in that index should not be added.
            while index in range(0, 5):

                if yellow_letters[index] == '':
                    pass

                elif yellow_letters[index] == word[index]:
                    yellow_letter_index_is_not_word_index = False
                    break

                index += 1

            # second: make sure that all yellow letters are somewhere in that word.
            for letter in letters_only:
                # if the # of times the letter is in the letter bank,
                # is the same as the # of times the letter is in the word or more, 
                # it's a valid word choice that should get added. 
                if word.count(letter) >= letters_only.count(letter) and letters_only.count(letter) >= 1:
                    pass
                else:
                    all_yellow_letters_are_in_word = False

            if yellow_letter_index_is_not_word_index and all_yellow_letters_are_in_word:
                updated_word_list.append(word)
        
        return updated_word_list, letters_only


def remove_grey_letters_from_word_list(word_list, green_letters, yellow_letters):

    updated_word_list = []

    grey_letters = get_grey_letters()

    if len(grey_letters) == 0:
        return word_list
    else: 
        for word in word_list:
            
            meets_grey_requirements = True

            for grey_letter in grey_letters:
                # if grey letter is already a green or yellow letter,
                # it can still be a valid word combination
                if grey_letter in word: 
                    if grey_letter in green_letters:
                        pass
                    elif grey_letter in yellow_letters:
                        pass
                    else:
                        meets_grey_requirements = False
                        break
            
            if meets_grey_requirements:
                updated_word_list.append(word) 

    return updated_word_list


# combine functions that update word lists to account for 
# green, yellow, and grey letters ...
# functions must be called in green -> yellow -> grey order
def update_word_list(word_list=wordle_words):

    # getting green_letters for checks in remove_grey_letters_from_word_list() ...
    # in case an additional grey letter is already a green letter
    green_words, green_letters = update_word_list_with_green_letters(word_list)

    green_yellow_words, yellow_letters = update_word_list_with_yellow_letters(green_words)

    green_yellow_grey_words = remove_grey_letters_from_word_list(green_yellow_words, green_letters, yellow_letters)

    return green_yellow_grey_words
    
    # TODO: with a proper interface, remove the last guess the user entered
    # from the list of possible word choices. 

def main():

    first_prompt = input("Do you want a suggestion for your first Wordle guess? \nY / N: ")

    if first_prompt.lower() == 'y':
        word_choices = get_word_choices()
        print("Here's what you should try guessing:")

        sleep(.5)

        for word in word_choices: 
            print(word.upper())
    if first_prompt.lower() == 'n':
        print("Guess your word and proceed.")

    sleep(.5)

    second_prompt = input("Still guessing your word? \nY / N: ")

    if second_prompt.lower() == 'y':
        still_guessing = True
    else:
        still_guessing = False

    # when going through the loop for the first time, 
    # the word list will be updated using the default word bank ...
    # for subsequent iterations, the word list will update itself
    counter = 0

    while still_guessing:
        if counter < 1:
            word_list = update_word_list(wordle_words)
        else:
            word_list = update_word_list(word_list)

        best_choices = get_word_choices(word_list)

        sleep(.5)

        print(f'There are {len(word_list)} possible word choices.')

        sleep(.5)

        if len(best_choices) == 1:
            print('The best word choice is:')
            for word in best_choices:
                print(word.upper())
        if len(best_choices) > 1:
            print('The best word choices are:')
            for word in best_choices:
                print(word.upper())

        sleep(.5)

        additional_prompts = input("Still guessing your word? \nY / N: ")

        if additional_prompts.lower() == 'y':
            pass
        else:
            guess_new_word = input('Would you like to guess a new word? \nY / N: ')

            if guess_new_word.lower() == 'y':
                main()
            else:
                return

        counter += 1

main()