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
        num, mod = mod, num % mod
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
    if a < 0 and b < 0:
        a, b = abs(a), abs(b)
    while (b != 0):
        if (b & 1): # Checks the last bit to see if odd or even
            product += a
            # print(a, b, product)
        a <<= 1
        b >>= 1
        # print(a, b)
    return product

def bitDivide(a, b):
    result = 0
    tempA = abs(a)
    tempB = abs(b)
    if b == 0: # Accounts for divide by zero case
        return None
    result = 0     
    while tempA >= tempB:
        tempA -= tempB
        result += 1
        # tempA = tempA << (result - 1)
    # print(tempA, tempB, result)    
    # print(power)
    if (a < 0 and b > 0)  or (b < 0 and a > 0):
        return 0 - result
    else:
        return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("\nUsage: %s <integer> <integer>\n" % sys.argv[0])
        
    a, b = int(sys.argv[1]), int(sys.argv[2])
    
    print(binaryMI(a, b))

