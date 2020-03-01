#Problem Set 8
#Intelligence course advisor
#Uses a greedy algorithm to determine an optimal course schedule

import time

SUBJECT_FILENAME = "subjects.txt"
SUBJECT_TRUNC = "subjects_trunc.txt"
VALUE, WORK = 0, 1
x=0
y=1
#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    sub_dict = {}
    sub_tup = ()
    sub_list = []
    sub_name = ""
    value = 0
    work = 0
    inputFile = open(filename)
    for line in inputFile:
        sub_list = line.split(",")
        sub_name = sub_list[0]
        value = sub_list[1]
        work = sub_list[2].strip('\n')
        sub_tup = (value,work)
        sub_dict[sub_name] = sub_tup
    return sub_dict
    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = sorted(subjects.keys())
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += int(val)
        totalWork += int(work)
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print (res)

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2

#
# Problem 2: Subject Selection By Greedy Optimization
#
def greedyAdvisor(subjects, maxWork, comparator):#this function was taken from a github. The implementatin of the comparator is incorrect. It doesn't utilize the decision tree model.
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.
    
    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """    

    # Build function that sorts based on comparator returns list of subject names sorted by comparator criteria.
    #
    global call_ctr
    def sort(l, comparator) :
        """
        Sorts the list of subjects' names in descendig order
        acording to the comparator.
        """
        # print "l, comparator type:", type(l), type(comparator)
        # print 
        
        for i in range(1, len(l)) :
            value = l[i]
            j = i - 1
            done = False
            # print 'i, value, j', i, value, j
            # print
            while not done:
                # print "subjects[value], subjects[l[j]] type:", type(subjects[value]), type(subjects[l[j]])
                # print
                if cmpValue(subjects[value], subjects[l[j]]):
                    l[j+1] = l[j]
                    j -= 1
                    if j < 0 :
                        done = True
                else :
                    done = True
            l[j+1] = value
    #
    # Pick classes from top of sorted list until maxWork is reached
    #
    schedule_list = [*subjects.keys()]
    #print 'schedule_list unsorted: ', schedule_list
    #print
    sort(schedule_list, comparator)
    # print 'schedule_list sorted: ', schedule_list
    #     print
    recommended_schedule = {}
    courseLoad = 0
    done = False
    for course in schedule_list:
        call_ctr+=1
        print("Subject:", course, "has value and work:", subjects[course])
        if int(subjects[course][WORK]) <= maxWork - courseLoad:
            recommended_schedule[course] = subjects[course]
            courseLoad += int(subjects[course][WORK])
        print("This is call #:",call_ctr)
    print ("Recommended tuples based on greedy algorithm:", printSubjects(recommended_schedule))
    return recommended_schedule


def record(key_rec,tup_rec): #my helper function
	choice_dict = {}
	choice_dict[key_rec] = tup_rec
	

def bruteForceAdvisor(subjects, maxWork):
    global call_ctr
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    start_time = time.time()
    nameList = [*subjects.keys()]
    tupleList = [*subjects.values()]
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    end_time = time.time()
    total_time = end_time - start_time
    print("Function took:", total_time, "to run.")
    print("Selection is:",printSubjects(outputSubjects))
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    global call_ctr
    call_ctr+=1
    print("This is call #:",call_ctr)
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if int(subsetWork) + int(s[WORK]) <= maxWork:
            #print(i)
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + int(s[VALUE]), subsetWork + int(s[WORK]))
            subset.pop()
            print ("Respectively: Subset, i, subsetValue, s[VALUE], subsetwork, s[WORK]",subset,i, subsetValue, s[VALUE],subsetWork,s[WORK])
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime():
    """
    Runs tests on bruteForceAdvisor and measures the time required to compute
    an answer.
    """

# Problem 3 Observations
# ======================
#
# TODO: write here your observations regarding bruteForceTime's performance

#
# Problem 4: Subject Selection By Dynamic Programming
#
def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    #we need make a 2d list to track the values selected by the advisor. fundamentally the advisor will be selecting
    #subjects on the basis of this:
    #if weight of subject <= maxWork:
    #max(value of subject at n-1, value of subject at n + value of subject 
    start_time = time.time()
    m={}
    final_dict={}
    values_list = []
    work_list = []
    nameList = [*subjects.keys()]
    tupleList = [*subjects.values()]
    for courses in subjects:
        values_list.append(subjects[courses][VALUE])
        work_list.append(subjects[courses][WORK])
    n = 0
    bestSubset, bestSubsetValue =  dp_helper(tupleList,maxWork,n,None,None,[],0,0,m)
    for i in bestSubset:
        final_dict[nameList[i]] = tupleList[i]
    end_time = time.time()
    total_time = end_time - start_time
    print("Function took:", total_time, "to run.")
    printSubjects(final_dict)
    return final_dict

def dp_helper(tupleList, maxWork, n, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork,m):
    global call_ctr
    call_ctr+=1
    print("This is call #:",call_ctr)
    #print ("Subset:",subset,"n:",n,"subsetValue:", subsetValue,"value(n):", tupleList[n][VALUE],"subsetWork:",subsetWork,"work(n):",tupleList[n][WORK])
    try: return m[(n,subsetWork)] 
    except KeyError:
        #if n == 0:
        #    if int(tupleList[n][WORK]) <= int(subsetWork):
        #        subset.append(n)
        #        m[(n,subsetWork)] = subset,tupleList[n][VALUE]
        #        print ("Subset:",subset,"n:",n,"subsetValue:", subsetValue,"value(n):", tupleList[n][VALUE],"subsetWork:",subsetWork,"work(n):",tupleList[n][WORK])
        #        return subset,tupleList[n][VALUE]
        #    else:
        #        m[(n,subsetWork)] = [],0
        #        print ("Subset:",subset,"n:",n,"subsetValue:", subsetValue,"value(n):", 0,"subsetWork:",subsetWork,"work(n):",0)
        #        return bestSubset, bestSubsetValue
        if n >= len(tupleList):
           if bestSubset == None or subsetValue > bestSubsetValue:
               # Found a new best.
               m[(n,subsetWork)] = subsetValue
               #print ("Subset:",subset,"n:",n,"subsetValue:", subsetValue,"value(n):", tupleList[n][VALUE],"subsetWork:",subsetWork,"work(n):",tupleList[n][WORK])
               return subset[:], subsetValue
           else:
               # Keep the current best.
               m[(n,subsetWork)] = bestSubsetValue
               #print ("Subset:",subset,"n:",n,"subsetValue:", subsetValue,"value(n):", tupleList[n][VALUE],"subsetWork:",subsetWork,"work(n):",tupleList[n][WORK])
               return bestSubset, bestSubsetValue
        else:
            s = tupleList[n]
            work = s[WORK]
            value = s[VALUE]
            # Try including subjects[i] in the current working subset.
            if int(subsetWork) + int(work) <= maxWork:
                #print(i)
                subset.append(n)
                bestSubset, bestSubsetValue = dp_helper(tupleList,
                        maxWork, n+1, bestSubset, bestSubsetValue, subset,
                        subsetValue + int(value), subsetWork + int(work),m)
                m[(n,subsetWork)] = bestSubset,bestSubsetValue
                print ("Subset:",subset,"n:",n,"subsetValue:", subsetValue,"value(n):", value,"subsetWork:",subsetWork,"work(n):",work)
                subset.pop() #return last item in subset
               
            bestSubset, bestSubsetValue = dp_helper(tupleList,
                    maxWork, n+1, bestSubset, bestSubsetValue, subset,
                    subsetValue, subsetWork,m)
            m[(n,subsetWork)] = bestSubset,bestSubsetValue
            print ("Subset:",subset,"n:",n,"subsetValue:", subsetValue,"value(n):", value,"subsetWork:",subsetWork,"work(n):",work) 
            return bestSubset, bestSubsetValue

# Problem 5: Performance Comparison
#
def dpTime():
    """
    Runs tests on dpAdvisor and measures the time required to compute an
    answer.
    """
    # TODO...
 
def get_nth_key(subjects, n):
    if n < 0:
        n += len(subjects)
    for i, key in enumerate(subjects.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 


# Problem 5 Observations
# ======================
#
# TODO: write here your observations regarding dpAdvisor's performance and
# how its performance compares to that of bruteForceAdvisor.
call_ctr = 0 
#subjects = loadSubjects(SUBJECT_FILENAME)
#sub_key_list = [*subjects.keys()]
#subInfo1 = subjects.get(sub_key_list[0])
#subInfo2 = subjects.get(sub_key_list[1])
subjects_trunc = loadSubjects(SUBJECT_TRUNC)
maxWork = 15 #set work capacity
#print(cmpWork(subInfo1, subInfo2))
#greedyAdvisor(subjects, maxWork, cmpValue(subInfo1,subInfo2))
bruteForceAdvisor(subjects_trunc,maxWork) #function runtime lower when maxWork is low. higher when maxWork is high.
call_ctr = 0 
dpAdvisor(subjects_trunc,maxWork)
