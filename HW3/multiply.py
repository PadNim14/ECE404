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

print(bitMult(-3 ,-9))
print(bitMult(10 ,80))
print(bitMult(-9 ,3))
