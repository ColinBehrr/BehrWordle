#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: colinbehr
"""

######################################################################
# Import two useful items.
from random import choice
from string import printable
 
######################################################################

def readWords(filename='words.dat'):
    with open(filename, 'r') as infile:
        S = infile.read().lower().split() # Words
    #print("{} words read.".format(len(S)))
    return(S)
 
######################################################################

def evalGuess(guess, target):
    fback = []   # Construct feedback
    pool = []    # Remaining unmatched target letters
 
    # Find matches between guess and target while building pool of
    # unmatched letters from target.
    for i in range(5):
        if guess[i] == target[i]:
            # Match; update fback.
            fback.append(guess[i].upper())
        else:
            fback.append('.')
            # Add unmatched target letter to pool.
            pool.append(target[i])

    for i in range(5):
        if guess[i] != target[i] and guess[i] in pool:
            # Match, but not in that position.
            fback[i] = guess[i]
            pool.pop(pool.index(guess[i]))
 
    # Splice the feedback back together and return it.
    return(''.join(fback))
 
######################################################################
# consistent(feedback, word) returns True if the feedback is
# consistent with word. 

def consistent(feedback: str, word: str) -> bool:
    letters_in_word = [*word]  # splitting the word into list of characters
    for letter in feedback:
        if letter != '.' and letter.isupper():
            # if the upper case letter is not there in the word = False
            if letter.lower() not in letters_in_word:
                return False
            else:
                # letter is there, so now pop the letter from the word
                letters_in_word.pop(letters_in_word.index(letter.lower()))
    # now checking for the lower case letters
    for letter in feedback:
        if letter != '.' and letter.islower():
            if letter not in letters_in_word:
                return False

    return True
                                    
######################################################################
# calcSize(S, feedback) returns the number of words in S that are
# consistent with the feedback provided.

def calcSize(S, feedback):
    count = 0
    for word in S:
        if consistent(feedback, word) == True:
            count = count + 1
        else:
            count = count
    return(count)
       
 
######################################################################

from random import choice
 
# Specification: wordle(S) takes a list of words, S, and randomly
# selects a target word for this round from S. It then manages game
# play, and returns True (meaning the user would like to play another
# round) or False (meaning that the user does not wish to play another
# round).

def wordle(S):
    target= choice(S)                                      # Random target word
    osize = len(S)                              # Initial size of dictionary
    feedback = '.'*5                                        # Initial feedback is empty
    avail = list(printable[10:36])    # List of available letters
    history = ""                                 # String history of word + feedback
    n = 6                                             # Remaining guesses
 
    # Print opening banner
    print('Welcome to Wordle!')
    print('Enter your guess, or ? for history; + for new game; or . to exit')
 
    # Repeat while guesses remain (or user quits with '+' or '.'
    # input). The general idea of this main game loop is to prompt the
    # user for a guess, then process the guess accordingly.
    while n > 0:
        # Uncomment the following line to enable "cheat mode." Cheat
        # mode reveals the usually hidden target word, making it
        # easier for you to debug your code.
        #print("Cheat: {}".format(target))  # Cheat mode!
 
        # Show available letters.
        print(''.join(avail))
 
        # Prompt the user for a guess.
        guess = input("\nWordle[{}]: '{}' >  ".format(7-n, feedback))
 
        # The next conditional statement breaks down game management
        # into an appropriately ordered series of outcomes.
        if guess in '.+':           # Abort game
            print("Abort game.\n{}The target word was {}\n".format(history, target))
            return(guess=='+')
        elif guess=='?':             # Show guess history
            print("History:\n{}".format(history))
            continue
        elif guess in history:                                # You've already guessed that!
            print('You have already guessed that!')
            continue
        elif guess not in S:        # Illegal guess
            print("Unrecognized word: '{}'".format(guess))
            continue
        elif not consistent(feedback, guess):
            print("Successive guesses must use all {} known hints.".format(5-feedback.count('.')))
            continue
 
        # Guess is legal and fits known feedback; accept the guess and
        # check it for the win.
        feedback = evalGuess(guess, target)
        history = history + " {}: {} => {}\n".format(7-n, guess, feedback)
        if feedback.lower() == target: # You win!
            print("Good job!\n{}The target word was {}\n".format(history, target))
            return(True)
 
        # Not a winner (yet): update status and try again.
        nsize = calcSize(S, feedback)              # new size
        print("Quality: {:.2%} [{} words remain]".format((osize - nsize + 1)/osize, nsize))
        osize = nsize
        feedback = evalGuess(guess,target)

        for i in range(len(guess)):
            if guess[i] in avail:
                if guess[i] in target:
                   avail[avail.index(guess[i])] = guess[i].upper()
                else:
                  avail[avail.index(guess[i])] = '.'

        # Go on to next guess
 
        n = n-1
 
    # If you get to this point, the user has run out of
    # guesses.
    print("Sorry, no dice...\n{}The target word was {}\n".format(history,target))
    # Assume they want to play another game.
    return(True)
 
######################################################################
# This code is executed automatically when you feed this file to a
# fresh invocation of Python. So, for example, from the Linux prompt:
#    > python hw1.py
# will start the game for interactive use right at the shell.
#
if __name__ == '__main__':
    # Read in the list of legal 5-letter words and then continue
    # playing the game until wordle() returns False.
    while wordle(S=readWords('words.dat')):
        print("Let's play again!\n")
