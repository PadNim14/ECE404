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
    if (a < 0 and b > 0)  or (b < 0 and a > 0):
        return 0 - result
    else:
        return result
    
print(bitDivide(8, -2))
print(bitDivide(9, 3))
print(bitDivide(15, 2))