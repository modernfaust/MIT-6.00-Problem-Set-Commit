#Problem Set 5 (Ghost)
#Create the word game ghost, as outlined by MIT 6.00 problenm set 5

import random

# -----------------------------------

import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print ("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print ("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()

# TO DO: your code begins here!

def check_word(word,word_list):
    lose_a = False
    lose_b = False
    if len(word) > 3:
        if word in word_list:
            print(word,"is a word!")
            lose_a = True
        else:
            for k in word_list:
                if len(word) < len(k) and k.find(word,0,len(word)) != -1:#if substring word is not found in k between 0 and length of substring
                    lose_a = False
                    break
                else:
                    #print("A. No word begins with",word)
                    lose_a = True
    elif len(word) == 2:
        for k in word_list:
                if k.find(word,0,2) != -1: #if substring word is not found in k between 0 and length of substring           
                    lose_b = False #this isn't working. Valid 2 char strings are triggering this
                    break
                else:
                    #print("B. No word begins with",word)
                    lose_b = True
    else:
        lose_a = False
    if lose_a == True and lose_b == False:
        print("A. No word begins with",word)
        return lose_a
    elif lose_a == False and lose_b == True:
        print("B. No word begins with",word)
        return lose_b
    else: 
        return False
def form_word(part_word,letter):
    new_word = part_word+letter
    return new_word

#def win(word,word_list):
#    player_win = False
#    if check_word(word,word_list) == True:
#        player_win = True
#        return player_win
#    elif check_word(word,word_list) == False:
#        player_win = False
#        return player_win

def determine_turn(ctr):
    if ctr%2 == 0 and ctr != 0:
        return 2
    else:
        return 1

def valid_input(letter):
    if letter in string.ascii_letters:
        return True
    else:
        return False

def conv_lower(letter):
    if letter in string.ascii_lowercase:
        return letter
    else:
        for i in range(0,len(string.ascii_uppercase)):
            if letter == string.ascii_uppercase[i]:
                return string.ascii_lowercase[i]
    
def ghost(word_list):
    word = ""
    letter = ""
    ctr = 0
    end = False
    player = 1
    print("Welcome to Ghost!")
    print("Player",player,"goes first.")

    while end == False:
        ctr +=1
        player = determine_turn(ctr)
        print("Current word fragment:",word)
        print("Player",player,"turn.")
        letter = input("Enter a letter: ")
        while valid_input(letter) is False:
            letter = input("Please enter a proper letter: ")
        letter = conv_lower(letter)
        word = form_word(word,letter)
        if check_word(word,word_list) == True:
            print ("Player", player, "loses!")
            print ("Player", determine_turn(ctr+1),"wins!")
            end = True

ghost(wordlist)
