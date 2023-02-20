#!/usr/bin/env python
# Homework Number: 5
# Name: Nimal Padmanabhan
# ECN Login: npadmana   
# Due Date: 2/21/23

from BitVector import *
from AES import AES_256_encrypt as encrypt, genTables


def x931(v0, dt, totalNum, key_file):
    '''
    * Arguments:
    v0: 128-bit BitVector object containing the seed value
    dt: 128-bit BitVector object symbolizing the date and time
    totalNum: The total number of random numbers to generate
    key_file: Filename for text file containing the ASCII encryption key for AES
    * Function Description:
    This function uses the arguments with the X9.31 algorithm to generate totalNum
    random numbers as BitVector objects.
    Returns a list of BitVector objects, with each BitVector object representing a
    random number generated from X9.31.
    '''
    randomNumList = []
    key = None
    with open(key_file) as f:
        key = f.read()
    key = key.strip()
    genTables()
    for _ in range(totalNum):
        ciphertext = encrypt(dt, key)
        temp = v0 ^ ciphertext
        rand_1 = encrypt(temp, key)
        randomNumList.append(rand_1)
        temp2 = rand_1 ^ ciphertext
        seed_temp = encrypt(temp2, key)
        v0 = seed_temp
    
    # Testing to see if the list has values of any kind    
    # for i in range(totalNum):
    #     print(randomNumList[i].get_bitvector_in_hex())
        
    return randomNumList    

        
    
    
    



