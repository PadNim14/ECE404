#!/usr/bin/env python
## BGCD.py
import sys

def binaryMI(num, mod):
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    # print(num, mod)
    while mod:
        # q = num // mod
        q = bitDivide(num, mod)
        # print(q)
        num, mod = mod, num % mod
        # print(num, mod)
        # x, x_old = x_old - q * x, x
        # print("x: "+str(x), "x_old: "+str(x_old))
        # print("y: "+str(y), "y_old: " +str(y_old))
        x, x_old = x_old - bitMult(x, q), x
        # y, y_old = y_old - q * y, y
        y, y_old = y_old - bitMult(y, q), y
       
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))
        

def bitMult(a, b):
    product = 0
    # Accounts for negative cases
    if a < 0 and b < 0:
        a, b = abs(a), abs(b)
    # B is repeatedly divided until it reaches 0 after doing bit shifts
    while (b > 0):
        if (b & 1): # Checks the last bit to see if odd or even
            product += a # If it is odd, the current value of a is added to the product variable
        a <<= 1 # a is left shifted by 1, which is the same as multiplying by 2
        b >>= 1 # b is right shifted by 1, which is the same as dividing by 2
    # If either number is negative, make the result of the product negative.
    # Otherwise, return the positive product
    if (a < 0 and b > 0)  or (b < 0 and a > 0):
        return 0-product
    else:
        return product


# Source: https://redquark.org/leetcode/0029-divide-two-integers/
def bitDivide(a, b):
    result = 0
    # In order to deal with negative numbers, make positive versions
    tempA = abs(a)
    tempB = abs(b)
    if b == 0: # Accounts for divide by zero case
        return None
    result = 0  # Serves as quotient variable
   
    while tempA >= tempB:
        # Idea: find the number of shifts until the temporary divisor is 
        # smaller than the temporary dividend
        n = 0 # Keeps track of number of shifts
        while tempA >= (tempB << n):
            n += 1
        # The number of times we shifted gets added to the result   
        result = result + (1 << (n - 1)) # result + 2^(n-1)
        # To account for the multiple of tempB that was added to tempA,
        # we subtract tempB from tempA and left shift that by n-1 places
        tempA -= tempB << (n - 1)
   
    # In order to account for negative results for division,
    # we check to see whether the divisor and/or dividend is negative
    # If it is, then we negate the result by doing 0 - result
    if (a < 0 and b > 0)  or (b < 0 and a > 0):
        return 0 - result
    else:
        return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("\nUsage: %s <integer> <integer>\n" % sys.argv[0])
        
    a, b = int(sys.argv[1]), int(sys.argv[2])

    binaryMI(a, b)

