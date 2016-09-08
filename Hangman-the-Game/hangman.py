"""Hangman the Game"""
#

# -----------------------------------
# Helper code

import random
import string

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print len(wordlist), "words loaded."
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    return all(i in lettersGuessed for i in secretWord)



def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    output = ''
    for i in secretWord:
        if i in lettersGuessed:
            output += i
        else:
            output += '_ '
    return output



def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    availables = string.ascii_lowercase
    for i in lettersGuessed:
        availables = availables.replace(i, '')
    return availables

# list to check the validity of raw input
alphabet_list = []
for i in string.ascii_lowercase:
    alphabet_list.append(i)
    
def visualizer(guesses): 
    if guesses == 0:
        print " _________     "
        print "|         |    "
        print "|         0    "
        print "|        /|\   "
        print "|        / \   "
    elif guesses == 1:
        print " _________     "
        print "|         |    "
        print "|         0    "
        print "|        /|\   "
        print "|        /     "
    elif guesses == 2:
        print " _________     "
        print "|         |    "
        print "|         0    "
        print "|        /|\   "
        print "|              "
    elif guesses == 3:
        print " _________     "
        print "|         |    "
        print "|         0    "
        print "|        /|    "
        print "|              "
    elif guesses == 4:
        print " _________     "
        print "|         |    "
        print "|         0    "
        print "|         |    "
        print "|              "
    elif guesses == 5:
        print " _________     "
        print "|         |    "
        print "|         0    "
        print "|              "
        print "|              "
    elif guesses == 6:
        print " _________     "
        print "|         |    "
        print "|              "
        print "|              "
        print "|              "
    elif guesses == 7:
        print " _________     "
        print "|              "
        print "|              "
        print "|              "
        print "|              "
    elif guesses == 8:
        print "               "
        print "|              "
        print "|              "
        print "|              "
        print "|              "
    print "|              "

# end of helper code
# -----------------------------------

def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.
    '''
    secretWord = secretWord.lower()
    print "\n------------"
    print "Welcome to the game, Hangman!"
    print "I am thinking of a word that is " + str(len(secretWord)) + " letters long."
    print "------------"
    lettersGuessed = []
    guesses = 8 # may change here to make it easier or harder
    while isWordGuessed(secretWord, lettersGuessed) is False and guesses > 0:
        print "You have " + str(guesses) + " guesses left"
        visualizer(guesses)
        print "Available letters: " + getAvailableLetters(lettersGuessed)
        letter = raw_input("Please guess a letter: ")
        letter = letter.lower()
        if letter not in alphabet_list:
            print "This is not a letter, try again! So far: " + getGuessedWord(secretWord, lettersGuessed)
        elif letter in lettersGuessed:
            print "Oops! You've already guessed that letter: " + getGuessedWord(secretWord, lettersGuessed)
        elif letter not in lettersGuessed:
            lettersGuessed.append(letter)
            if letter in secretWord:
                print "Good guess: " + getGuessedWord(secretWord, lettersGuessed)
            else:
                guesses -= 1
                print "Oops! That letter is not in my word: " + getGuessedWord(secretWord, lettersGuessed)
        print "------------"

    if isWordGuessed(secretWord, lettersGuessed):
        print "Congratulations, you won!"
    elif guesses == 0:
        print "Sorry, you ran out of guesses. The word was " + secretWord + "."

    choice = ''
    while not (choice == 'y' or choice == 'n'):
        choice = raw_input("Do you want to play again? (y/n): ")
        choice = choice.lower()
        if choice == 'y':
            secretWord = chooseWord(wordlist).lower()
            hangman(secretWord)
        elif choice == 'n':
            print "Good bye!"
        else:
            print "This is not a valid choice!"


secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
