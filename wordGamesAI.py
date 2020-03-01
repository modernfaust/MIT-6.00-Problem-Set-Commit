#Problem 6
#An extention of the problem 5 word game, with an algorithm that selects based on max word scores per hand

import random
import string
import time
import itertools

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------

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

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # TO DO ...
    sum = 50
    ctr = 0
    for i in range (0,len(word)):
        sum+=SCRABBLE_LETTER_VALUES.get(word[i])
        ctr+=1
    if n-ctr > 0:
        sum-=50
    return sum
#
# Make sure you understand how this function works and what it does!

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print (letter,)              # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(int(num_vowels)):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(int(num_vowels), n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    your_word=get_frequency_dict(word)
    updated_hand=hand
            
    for letter,quant in your_word.items():
        if your_word[letter] > 0:
            updated_hand[letter] = updated_hand.get(letter,0)-your_word.get(letter,0)
    return updated_hand

# Problem #3: Test word validity
#
def is_valid_word(word, hand, points_dict):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # TO DO ...
    is_valid = False
    word_dict = get_frequency_dict(word)
    #print(word_dict)
    if word in points_dict:
        for key in word_dict:
            if word_dict.get(key) > hand.get(key,0):
                is_valid = False
                return is_valid
            else:
                is_valid = True
    else:
        print("Word not in word list.")
        return False

    return is_valid

def get_time_limit(points_dict, k):

# Return the time limit for the computer player as a function of the
#multiplier k.
# points_dict should be the same dictionary that is created by
#get_words_to_points.

    start_time = time.time()
    # Do some computation. The only purpose of the computation is so we can
    # figure out how long your computer takes to perform a known task.
    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE)
        end_time = time.time()
    
    return (end_time - start_time) * k 

#
# Problem #4: Playing a hand
#
def get_words_to_points(word_list):
#Return a dict that maps every word in word_list to its point value. 
    points_dict = {}
    vowels_y = VOWELS + CONSONANTS[19]
    ctr = 0
    for word in word_list:
        points_dict[word] = get_word_score(word,HAND_SIZE)
    return points_dict

def get_word_rearrangement(word_list):#this was taken from the answer set
    """
    return a dict which the keys are string containing the letters of word in sorted order,
    and the values are the word.
    """
    rearrange_dict = {}
    store_a = ''
    sorted_word_string = ''
    #for word in word_list: #my implementation of the below code. this is incredibly inefficient.
    #    for i in range(len(word),0,-1):
    #        store_a += word[i-1]
    #    rearrange_dict[store_a] = word
    #    print(rearrange_dict[store_a])

    for word in word_list: #most efficient implementation
        sorted_word_string = ''.join(sorted(word)) #sorted(word) is built in func to alphabetize
        rearrange_dict[sorted_word_string] = word
    #print (rearrange_dict)
    return rearrange_dict

    #rearrange_dict = {} #another solution set code
    #for word in word_list:
    #    #   build a list from the char in word: 1) convert word string to list, 2) sort list, 3) convert list back to string.
    #    char_list =[]
    #    my_string = ''
    #    for char in word:
    #        char_list.append(char)
    #    char_list.sort()
    #    for each in range(len(char_list)):
    #        my_string +=char_list[each]
    #    rearrange_dict[my_string] = word
    #print ("In get_word_rearrangements. Rrearrange_dict:", rearrange_dict)
    #return rearrange_dict

def pick_best_word(hand,points_dict):
    """
 Return the highest scoring word from points_dict that can be made with the
given hand.
  Return '.' if no words can be made with the given hand.
""" 
    #this is a O(x) algorithm because it scales based on length of hand. The larger the number of keys in hand,
    #the more you have to search for. The fewer the letters in hand, the quicker the run time.
    total = 0
    best_word = ""
    display_hand(hand)
  
    for key in points_dict:
        if sum(hand.values()) >= len(key) and is_valid_word(key,hand,points_dict) == True:
            #print("Word: ",key,"Value: ", points_dict.get(key,0))
            if total <= points_dict.get(key,0):
                total = points_dict.get(key)
                best_word = key
    print("Best word is",best_word, "", points_dict.get(best_word,0))
    return best_word

def pick_best_word_faster(hand, rearrange_dict):
    #this is a O(1) algorithm. It is simply a lookup operation that looksup words in the dictionary.
    #Through time tests, this seems to yield roughly the same each run, in spite of the length of hand
    w = ''
    store_a = 0
    hand_subsets = ()
    best_word = ''
    letters = [c for c in hand for i in range(hand[c])]
    #letters = [] #this is my implementation of the above line
    #for c in hand:
    #    for i in range(hand[c]):
    #        letters += c
    #print(letters)
    for i in range(1, len(letters)+1):
        for tup in set(itertools.combinations(letters, i)):
            hand_subsets += (''.join(sorted(tup)), )

    for s in hand_subsets:
        w = ''.join(sorted(s))
        if w in rearrange_dict and get_word_score(s,sum(hand.values())) >= store_a:
            store_a = get_word_score(w,sum(hand.values()))
            best_word = rearrange_dict[w]
            print (w,best_word, store_a)
    print ("Best word is:", best_word, "with value", store_a)
    return s


def play_hand(hand, points_dict,rearrange_dict):
    updated_hand = hand
    word_dict = {}
    final_score = 0
    total = 0
    valid_word = False
    start_time = time.time()
    buzzer = input("Enter time limit, in seconds, for players: ")
    k = 2

    while len(updated_hand) > 0:
        display_hand(updated_hand)
        while True:
            word = input("Enter your word. Press f to test the AI. Press g to test the improved AI. To exit, please press '.'")
            end_time = time.time()
            total_time = end_time - start_time
            computer_time = get_time_limit(points_dict, k)#record time limit for AI
            remainder = float(buzzer) - total_time
            print ('It took %0.2f to enter a word' % total_time)
            if word == ".":
                return total
            if word == 'f': #to pilot the AI function
                print('AI max time is:',computer_time)
                start_time = time.time()#to record the computer's time
                k=1
                computer_time = get_time_limit(points_dict, k)
                pick_best_word(updated_hand,points_dict)
                end_time = time.time()
                total_time = end_time - start_time
                remainder = float(computer_time)-total_time
                print ('It took the AI %0.2f to enter a word' % total_time)
            if word == 'g': #to pilot the improved AI function
                print('AI max time is:',computer_time)
                start_time = time.time()#to record the computer's time
                k=1
                computer_time = get_time_limit(rearrange_dict, k)
                pick_best_word_faster(updated_hand,rearrange_dict)
                end_time = time.time()
                total_time = end_time - start_time
                remainder = float(computer_time)-total_time
                print ('It took the AI %0.2f to enter a word' % total_time)
            if remainder > 0:
                print("You have ",remainder," seconds remaining")
            else:
                print("Time's out!")
                break
            if len(word) > HAND_SIZE or is_valid_word(word,updated_hand,points_dict) == False:
                print("Invalid word. Please try again")
            else:
                break
        word_dict = get_frequency_dict(word)
        updated_hand = update_hand(updated_hand,word)
        final_score = (get_word_score(word,len(word)))
        total += final_score
        print("You scored:",final_score,"points! You currently have:",total,"points!")
    print("Your total score is:",total)
# Problem #5: Playing a game
# Make sure you understand how this code works!
def play_game(word_list,rearrange_dict):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    
    hand = deal_hand(HAND_SIZE) # random init
    points_dict = get_words_to_points(word_list)
    while True:
        cmd = input('enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand, points_dict,rearrange_dict)
            print()
        elif cmd == 'r':
            play_hand(hand, points_dict,rearrange_dict)
            print()
        elif cmd == 'e':
            break
        #elif cmd == 'f':
        #    hand = deal_hand(HAND_SIZE)
        #    pick_best_word(hand,points_dict,rearrange_dict)
        #    print()
        else:
            print ("invalid command.")

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words() #original words_list
    points_dict = get_words_to_points(word_list) #generate dict mapping values to word-score
    rearrange_dict = get_word_rearrangement(word_list)
    play_game(points_dict,rearrange_dict)
    #get_words_to_points(word_list)
    #get_hand_subsets(deal_hand(HAND_SIZE))
    #get_word_rearrangement(word_list)
    #pick_best_word_faster(deal_hand(HAND_SIZE), rearrange_dict)
