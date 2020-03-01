#Problem Set 3
#An exercise in Python string manipulation
#constrainedMatchPair
from string import *
def subStringMatchExact(target,key):
    matches = ()
    start = 0
    while target.find(key,start) != -1:
        start = target.find(key,start)
        matches+=(start,)
        start +=1
    #print (matches)
    return matches

def constrainedMatchPair(firstMatch, secondMatch, length):
    constrained_matches = ()
    k = 0
    #check all elements of second tuple with all potential values of k
    for i in range (len(firstMatch)):
        k = firstMatch[i]+length+1
        for x in range  (len(secondMatch)):
            if k == secondMatch[x]:
                constrained_matches+=(k,)
    return constrained_matches

def subStringMatchOneSub(key,target):
    """search for all locations of key in target, with one substitution"""
    allAnswers = ()
    for miss in range(0,len(key)):
        # miss picks location for missing element
        # key1 and key2 are substrings to match
        key1 = key[:miss]
        key2 = key[miss+1:]
        print ("breaking key",key,"into",key1,key2)
        # match1 and match2 are tuples of locations of start of matches
        # for each substring in target
        match1 = subStringMatchExact(target,key1)
        match2 = subStringMatchExact(target,key2)
        # when we get here, we have two tuples of start points
        # need to filter pairs to decide which are correct
        filtered = constrainedMatchPair(match1,match2,len(key1))
        allAnswers = allAnswers + filtered
        print ("match1",match1)
        print ("match2",match2)
        print ("possible matches for",key1,key2,"start at",filtered)
    return allAnswers

def subStringMatchExactlyOneSub(target,key): 
    answer_tuple = ()
    if len(key) <= 1:
        answer_tuple = subStringMatchExact(target,key)
        return answer_tuple
    else:
        for miss in range(1,len(key)):
        # need to split the key
            key1 = key[:miss]
            key2 = key[miss+1:]
        # match1 and match2 are tuples of locations of start of matches
        # for each substring in target
            match1 = subStringMatchExact(target,key1)
            match2 = subStringMatchExact(target,key2)
            filtered = constrainedMatchPair(match1,match2,len(key1))
            answer_tuple = answer_tuple + filtered
        # when we get here, we have two tuples of start points
        # need to filter pairs to decide which are correct
    return answer_tuple

target = "ATGACATGCACAAGTATGCAT"
key = "ACBT"
key1 = "AC"
key2 = "T"
#print(subStringMatchExact(target,key1))
#print(subStringMatchExact(target,key2))
#-------the below is used to launch constrained Match pair (Problem 3)
#start1 = subStringMatchExact(target,key1)
#start2 = subStringMatchExact(target,key2)
#print(constrainedMatchPair(start1,start2,len(key1)))
#-------the below is used to launch the check function
#print(subStringMatchOneSub(key,target))
#-------the below answers Problem 4, which asks to filter all searches so that we match the key with exactly ONE substitute letter, not 0
print(subStringMatchExactlyOneSub(target,key))
        
