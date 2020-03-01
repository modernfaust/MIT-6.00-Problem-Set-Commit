#Problem Set 4
#A small simulation of a retirement fund, with an implementation of binary search

def nestEggFixed(salary, save, growthRate, years):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: the annual percent increase in your investment account (an
      integer between 0 and 100).
    - years: the number of years to work.
    - return: a list whose values are the size of your retirement account at
      the end of each year.
    """
    retireAccount = []
    retireAccount.append(salary*save*0.01)
    for i in range (0,years):
        retireAccount.append(retireAccount[i]*(1+0.01*growthRate)+(salary*save*0.01))
    return retireAccount

def testNestEggFixed():
    salary     = 10000
    save       = 10
    growthRate = 15
    years      = 5
    savingsRecord = nestEggFixed(salary, save, growthRate, years)
    print (savingsRecord)
    # Output should have values close to:
    # [1000.0, 2150.0, 3472.5, 4993.375, 6742.3812499999995]

def nestEggVariable(salary, save, growthRates):
    retireAccount = []
    retireAccount.append(salary*save*0.01)
    years = len(growthRates)-1
    for i in range (0,years):
        retireAccount.append(retireAccount[i]*(1+0.01*growthRates[i])+(salary*save*0.01))
    return retireAccount

def testNestEggVariable():
    salary      = 10000
    save        = 10
    growthRates = [3, 4, 5, 0, 3]
    savingsRecord = nestEggVariable(salary, save, growthRates)
    print (savingsRecord)
    # Output should have values close to:
    # [1000.0, 2040.0, 3142.0, 4142.0, 5266.2600000000002]

def postRetirement(savings, growthRates, expenses):
    """
    - savings: the initial amount of money in your savings account.
    - growthRate: a list of the annual percent increases in your investment
      account (an integer between 0 and 100).
    - expenses: the amount of money you plan to spend each year during
      retirement.
    - return: a list of your retirement account value at the end of each year.
    """
    retireAccount=[]
    years = len(growthRates)
    retireAccount.append(savings*(1+0.01*growthRates[0])-expenses)
    for i in range (1,years):
        retireAccount.append(retireAccount[i-1]*(1+0.01*growthRates[i])-expenses)
    return retireAccount

def testPostRetirement():
    savings     = 100000
    growthRates = [10, 5, 0, 5, 1]
    expenses    = 30000
    savingsRecord = postRetirement(savings, growthRates, expenses)
    print (savingsRecord)
    # Output should have values close to:
    # [80000.000000000015, 54000.000000000015, 24000.000000000015,
    # -4799.9999999999854, -34847.999999999985]


def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates,
                    epsilon):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - preRetireGrowthRates: a list of annual growth percentages on investments
      while you are still working.
    - postRetireGrowthRates: a list of annual growth percentages on investments
      while you are retired.
    - epsilon: an upper bound on the absolute value of the amount remaining in
      the investment fund at the end of retirement.
    """
    fundSize = nestEggVariable(salary, save, preRetireGrowthRates)[-1]
    print("Amount of Savings: ",fundSize)
    ctr = 0
    low = 0
    high = fundSize+epsilon
    guess = (low+high)/2
    check = postRetirement(fundSize,postRetireGrowthRates,guess)[-1]
    print("Pre-run: ", guess, ",", check)
    while check > epsilon or check < 0:
        ctr+=1
        check = postRetirement(fundSize,postRetireGrowthRates,guess)[-1]
        print("Estimate",ctr,": ",guess,", yields a final savings of: ",check)
        if check > 0:
           low = guess
        else:
           high = guess
        guess = (low+high)/2
    return guess
def testFindMaxExpenses():
    salary                = 10000
    save                  = 10
    preRetireGrowthRates  = [3, 4, 5, 0, 3]
    postRetireGrowthRates = [10, 5, 0, 5, 1]
    epsilon               = .01
    expenses = findMaxExpenses(salary, save, preRetireGrowthRates,
                               postRetireGrowthRates, epsilon)
    print (expenses)
    # Output should have a value close to:
    # 1229.95548986
testFindMaxExpenses()
