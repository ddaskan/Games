from scrabble_v1 import *
import time

def CanBeConstructed(word, hand):
    """
    Returns True if word entirely composed of 
    letters in the hand. Otherwise, returns False.

    Does not mutate hand.
   
    word: string
    hand: dictionary (string -> int)
    """
    word_dict = getFrequencyDict(word)
    for i in word_dict.keys():
        if word_dict[i] > hand.get(i, 0):
            return False
    return True

def compChooseWord(hand, wordList, n):
    """
    Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None
    """
    # Create new variables to store the maximum score seen so far (initially 0) and the best word seen so far (initially None)  
    best_score = 0 
    best_word = None

    # For each word in the wordList
    for word in wordList:

        # If can construct the word from your hand
        if CanBeConstructed(word, hand):

            # Find out how much making that word is worth
            temp = getWordScore(word, n)

            # If the score for that word is higher than your best score
            if temp > best_score:

                # Update your best score, and best word accordingly
                best_score = temp
                best_word = word

    # return the best word found.
    return best_word


def compPlayHand(hand, wordList, n):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).
 
    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    score = 0
    print 
    while compChooseWord(hand, wordList, n) != None:
        print ('Current Hand:'), 
        displayHand(hand)
        
        word = compChooseWord(hand, wordList, n)
        point = getWordScore(word, n)
        score += point
        print ('"') + word + ('" earned ') + str(point) + (' points. Total: ') + str(score) + (' points\n')
        
        hand = updateHand(hand, word)
    
    if calculateHandlen(hand) > 0:
        print ('Current Hand:'), 
        displayHand(hand)    
    print ('Total score: ') + str(score) + (' points.')
 
"""  
# Test cases for compPlayHand()
print "-------------------------------"
compPlayHand({'a': 1, 'p': 2, 's': 1, 'e': 1, 'l': 1}, wordList, 6)
print "-------------------------------"
compPlayHand({'a': 2, 'c': 1, 'b': 1, 't': 1}, wordList, 5)
print "-------------------------------"
compPlayHand({'a': 2, 'e': 2, 'i': 2, 'm': 2, 'n': 2, 't': 2}, wordList, 12)
""" 

def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
      
        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    wordList: list (string)
    """
    n = HAND_SIZE
    hand = ''
    while True:
        input = raw_input('\nEnter n to deal a new hand, r to replay the last hand, or e to end game: ')
        input = input.lower()
        if input == 'e':
            break
        elif not (input == 'n' or input == 'r'):
            print ('Invalid command.')
        elif input == 'r' and hand == '':
            print ('You have not played a hand yet. Please play a new hand first!')
        else:
            while True:
                input2 = raw_input('\nEnter u to have yourself play, c to have the computer play: ')
                input2 = input2.lower()
                if not (input2 == 'c' or input2 == 'u'):
                    print ('Invalid command.')
                elif input == 'n' and input2 == 'u':
                    hand = dealHand(n)
                    playHand(hand, wordList, n)
                    break
                elif input == 'n' and input2 == 'c':
                    hand = dealHand(n)
                    compPlayHand(hand, wordList, n)
                    break
                elif input == 'r' and input2 == 'c':
                    compPlayHand(hand, wordList, n)
                    break
                elif input == 'r' and input2 == 'u':
                     playHand(hand, wordList, n)
                     break


if __name__ == '__main__':
    print "#### WELCOME the SCRABBLE ####\n"
    wordList = loadWords()
    playGame(wordList)
