#Problem Set 1
#A program that generates the 1000th prime number, following the generate and test method
from math import *

#-This is to count primes up to the 1000th prime
x=0
y=0
prime_count = 0
factor = 0
while prime_count < 1000:
	while y < x:
		y+=1
		if x%y == 0:
			factor+=1
	if factor == 2:
		prime_count += 1
		print ('Prime #:', + prime_count,' is ', + x)
	x = x+1
	factor = 0
	y = 0

#-This is to compute the sum of log of primes less than n
#x=0
#y=0
#n=300
#prime_count = 0
#factor = 0
#sum = 0
#while x < n:
#	while y < x:
#		y = y+1	
#		if x%y == 0:
#			factor += 1
#	if factor  == 2:
#		sum += log(x)
#		prime_count += 1
#	x += 1
#	factor = 0
#	y = 0
#print ('The sum of the log of primes up to n is', + sum)
#print ('n = ', + n)
#print ('The ratio of the sum of log(x) up to n is: ', + sum/n)

#Another logsum test
#logsum = 0
#n = 5
#for x in range(2,n):                            #picks numbers to test
#    for divisor in range(2, 1+int(sqrt(x+1))):
#        if x%divisor == 0:                      #checks if x is prime
#            break
#    else:
#        logsum += log(x)
#print ('The sum of the log of primes up to n is', + logsum)
#print ('n = ', +n)
#print ('The ratio of the sum of log(x) up to n is: ', + logsum/n)

#Test to see if above code generates proper prime numbers less than n
#logsum = 0
#n = 47
#for x in range(2,n):                            #picks numbers to test
#    for divisor in range(2, 1+int(sqrt(x+1))):
#        if x%divisor == 0:                      #checks if x is prime
#            break
#    else:
#        logsum += log(x)
#        print (x)
#print ('The sum of the log of primes up to n is', + logsum)
#print ('n = ', +n)
#print ('The ratio of the sum of log(x) up to n is: ', + logsum/n)
