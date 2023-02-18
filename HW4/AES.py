#!/usr/bin/env python
# Homework Number: 4
# Name: Nimal Padmanabhan
# ECN Login: npadmana   
# Due Date: 2/14/23

##  Adapted from Avi Kak's AES code snippets
##  Avi Kak  (April 10, 2016; bug fix: January 27, 2017; doc errors fixed: February 2, 2018)


##  It will also prompt you for a key.  If the key you enter is shorter
##  than what is needed for the AES key size, we add zeros on the right of
##  the key so that its length is as needed by the AES key size.

import sys
from BitVector import *
import copy

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption                                            
invSubBytesTable = []                                               # for decryption     
e_const = BitVector(intVal=0x0e)
b_const = BitVector(intVal=0x0b)
d_const = BitVector(intVal=0x0d)
nine_const = BitVector(intVal=0x09)                

def AES_256():
    encDec = sys.argv[1]
    outputFile = sys.argv[4]

    if encDec == '-e':
        messageFile = sys.argv[2]
        AES_256_encrypt(messageFile, outputFile)
        
    elif encDec == '-d':
        encryptedFile = sys.argv[2]
        AES_256_decrypt(encryptedFile, outputFile)
            
            
def AES_256_encrypt(filename, outputFile):
    key_bv = get_key_from_file(sys.argv[3])
    key_words = gen_key_schedule_256(key_bv)
    # print(key_words[0].get_bitvector_in_hex())
    num_rounds = 14
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])

    # print(round_keys[0].get_bitvector_in_hex())
    # print(len(round_keys))
    genTables()
    bv = BitVector(filename=filename) 
    OUT = open(outputFile, 'w')
    # tempOUT = open("temp.txt", 'w')
    # Shift rows
    state_array = [[0 for x in range(4)] for x in range(4)]
    # bitvec = BitVector()
    # sub_bytes_table = gen_subbytes_table()
    
    while bv.more_to_read:
        bitvector = bv.read_bits_from_file(128)
        if len(bitvector) > 0:
            if len(bitvector) != 128:
                bitvector.pad_from_right(128 - len(bitvector))
            # Populating state array with bitvector and XORing them with first 4 keywords...
            bitvector ^= round_keys[0]
            # print("First plaintext block: " + bitvector.get_bitvector_in_hex())
            state_array = [[0 for x in range(4)] for x in range(4)]
            
            for i in range(4):
                for j in range(4):
                    state_array[j][i] = bitvector[32*i + 8*j : (32*i + 8*(j+1))].intValue()
                   
            for round in range(num_rounds - 1):
                # Substitute bytes
                # print(state_array)
                state_array = sub_bytes(state_array)
                # print(state_array)
                # state_array = inv_sub_bytes(state_array)
                # print(state_array)
                # sys.exit()
                tempbv = BitVector(size=0)
                for i in range(4):
                    for j in range(4):
                        tempbv += BitVector(intVal=state_array[j][i], size=8)
                # print(("After sub-bytes: " + str(tempbv.get_bitvector_in_hex())))
                
                # Shift rows
                
                state_array = shift_rows(state_array)
               
                
                # state_array = inv_shift_rows(state_array)
                # print(state_array)
                # print("------------------------------------")
                # sys.exit()
                
                tempbv = BitVector(size=0)
                for i in range(4):
                    for j in range(4):
                        tempbv += BitVector(intVal=state_array[j][i], size=8)
                # print(("After shift rows: " + str(tempbv.get_bitvector_in_hex())))
                
                
                # Mix columns, but not in the last round
                # print(state_array)
                two_const = BitVector(bitstring="000000010")
                three_const = BitVector(bitstring="00000011")
                state_array = mix_columns(state_array, two_const, three_const)
               
                tempbv = BitVector(size=0)
                
                one_state_array = add_round_keys(state_array, round_keys, round)
                # print(one_state_array)
                # for i in range(4):
                #     for j in range(4):
                #         # state_array[j][i] = one_state_array[32*j + 8*i : (32*j + 8*(i+1))].intValue()
                #         state_array[j][i] = one_state_array[32*i + 8*j : (32*i + 8*(j+1))].intValue()
               
                for i in range(4):
                    for j in range(4):
                        # state_array[j][i] = one_state_array[32*j + 8*i : (32*j + 8*(i+1))].intValue()
                        state_array[j][i] = one_state_array[32*i + 8*j : (32*i + 8*(j+1))].intValue()
                # print(state_array)
                
            
            # Sub bytes            
            state_array = sub_bytes(state_array)
            
            # Shift rows
            state_array = shift_rows(state_array)
            
            # Add round keys
            state_array = add_round_keys(state_array, round_keys, 13)
            
            # print("After round key: " + str(state_array.get_bitvector_in_hex()))
            # sys.exit()
            OUT.write(state_array.get_bitvector_in_hex())
        # write_encrypted_file(state_array, OUT)
    OUT.close() 
                  

   
def AES_256_decrypt(filename, outputFile):
    key_bv = get_key_from_file(sys.argv[3])
    key_words = gen_key_schedule_256(key_bv)
    # for word in key_words:
    #     print(word.get_bitvector_in_hex())
    # print(key_words)
    # print(key_words[0].get_bitvector_in_hex())
    num_rounds = 14
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])
    round_keys_rev = round_keys[::-1]
    # for key in round_keys_rev:
    #     print(key.get_bitvector_in_hex())
    # print(round_keys)
    genTables()
    FILE = open(filename, 'r')
    bv = BitVector(hexstring=FILE.read())
    OUT = open(outputFile, 'w')
   
    state_array = [[0 for x in range(4)] for x in range(4)]

    
    for i in range(len(bv) // 128):
        bitvector = bv[i * 128 : (i + 1) * 128]
        if len(bitvector) > 0:
            if len(bitvector) != 128:
                bitvector.pad_from_right(128 - len(bitvector))
            # Populating state array with bitvector and XORing them with first 4 keywords...
            bitvector ^= round_keys_rev[0]
            # print(round_keys_rev[0])
            # print("First plaintext block: " + bitvector.get_bitvector_in_hex())           
                 
            for round in range(num_rounds - 1):
                state_array = [[0 for x in range(4)] for x in range(4)]
            
                for i in range(4):
                    for j in range(4):
                        state_array[j][i] = bitvector[32*i + 8*j : (32*i + 8*(j+1))].intValue()
                # Shift rows
                # print(state_array)
                state_array = inv_shift_rows(state_array)
               
                # print(state_array)
                # sys.exit()
                state_array = inv_sub_bytes(state_array)
                # print(state_array)
                one_state_array = inv_add_round_keys(state_array, round_keys_rev, round)
                for i in range(4):
                    for j in range(4):
                        state_array[j][i] = one_state_array[32*i + 8*j : (32*i + 8*(j+1))].intValue()
                        
                state_array = inv_mix_columns(state_array, e_const, b_const, d_const, nine_const)
                # print(state_array)
                tmp1 = BitVector(size = 0)
                for i in range(4):
                    for j in range(4):
                        # print(tmp1.get_bitvector_in_ascii())
                        # print(state_array[j][i])
                        tmp1 += BitVector(intVal=state_array[j][i], size=8)
                # sys.exit()
                bitvector = tmp1
                # print(tmp1.get_bitvector_in_ascii())
                # sys.exit()
            # Inverse Shift rows
            state_array = inv_shift_rows(state_array)
            # Inverse Sub bytes            
            state_array = inv_sub_bytes(state_array)
            # Inverse Add round keys
            state_array1 = inv_add_round_keys(state_array, round_keys_rev, 13)
            print(state_array1.get_bitvector_in_ascii())
            
            
        OUT.write(state_array1.get_bitvector_in_ascii())
       
    OUT.close() 
    FILE.close()
        

def sub_bytes(state_array):
    # Substitute bytes
    # print(subBytesTable)
    for i in range(4):
        for j in range(4):
            # state_array[j][i] = BitVector(intVal=(sub_bytes_table[int(state_array[j][i])]))
            temp = int(state_array[i][j])
            value = subBytesTable[temp]
            
            # state_array[j][i] = BitVector(intVal=(sub_bytes_table[(state_array[j][i])]), size=8)
            state_array[i][j] = value
            
    return state_array

def inv_sub_bytes(state_array):
    for i in range(4):
        for j in range(4):
        # state_array[j][i] = BitVector(intVal=(sub_bytes_table[int(state_array[j][i])]))
            temp = int(state_array[i][j])
            value = invSubBytesTable[temp]
        
        # state_array[j][i] = BitVector(intVal=(sub_bytes_table[(state_array[j][i])]), size=8)
            state_array[i][j] = value
        
    return state_array


def shift_rows(state_array):
    temp = copy.deepcopy(state_array)
    for i in range(1, 4):
        for j in range(4):
            # s0.0 s0,1 s0,2 s0,3
            # s1.1 s1,2 s1,3 s1,0
            # s2.2 s2,3 s2,0 s2,1
            # s3.3 s3,0 s3,1 s3,2
            temp[i][j] = state_array[i][(j + i) % 4]   
    return temp   

def inv_shift_rows(state_array):
    temp = copy.deepcopy(state_array)
    for i in range(1, 4):
        for j in range(4):
            # s0.0 s0,1 s0,2 s0,3
            # s1.1 s1,2 s1,3 s1,0
            # s2.2 s2,3 s2,0 s2,1
            # s3.3 s3,0 s3,1 s3,2
            temp[i][j] = state_array[i][(j - i) % 4]   
    return temp   

def mix_columns(state_array, two_const, three_const):
    newStateArray = copy.deepcopy(state_array)
    for j in range(4):
        # print(type(state_array[2][j]))
        # s′0,j = (0x02 × s0,j) ⊗ (0x03 × s1,j ) ⊗ s2,j ⊗ s3,j
        # print(state_array)
        state_array[0][j] = BitVector(intVal=state_array[0][j], size=8)
        state_array[1][j] = BitVector(intVal=state_array[1][j], size=8)
        state_array[2][j] = BitVector(intVal=state_array[2][j], size=8)
        state_array[3][j] = BitVector(intVal=state_array[3][j], size=8)
        # newStateArray = [[0 for x in range(4)] for x in range(4)]
        
        
        newStateArray[0][j] = (state_array[0][j].gf_multiply_modular(two_const, AES_modulus, 8)) ^ (state_array[1][j].gf_multiply_modular(three_const, AES_modulus, 8)) ^ state_array[2][j] ^ state_array[3][j]
        newStateArray[1][j]  = (state_array[0][j] ^ (state_array[1][j].gf_multiply_modular(two_const, AES_modulus, 8))) ^ (state_array[2][j].gf_multiply_modular(three_const, AES_modulus, 8)) ^ state_array[3][j]
        newStateArray[2][j] = state_array[0][j] ^ state_array[1][j] ^ (state_array[2][j].gf_multiply_modular(two_const, AES_modulus, 8)) ^ (state_array[3][j].gf_multiply_modular(three_const, AES_modulus, 8))
        newStateArray[3][j]  = (state_array[0][j].gf_multiply_modular(three_const, AES_modulus, 8)) ^ state_array[1][j] ^ state_array[2][j] ^ (state_array[3][j].gf_multiply_modular(two_const, AES_modulus, 8))
        
        
        newStateArray[0][j] = newStateArray[0][j].intValue()
        newStateArray[1][j] = newStateArray[1][j].intValue()
        newStateArray[2][j] = newStateArray[2][j].intValue()
        newStateArray[3][j] = newStateArray[3][j].intValue()
    return newStateArray

def inv_mix_columns(state_array, e_const, b_const, d_const, nine_const):
    newStateArray = copy.deepcopy(state_array)
    for j in range(4):
        # print(type(state_array[2][j]))
        # s′0,j = (0x02 × s0,j) ⊗ (0x03 × s1,j ) ⊗ s2,j ⊗ s3,j
        # print(state_array)
        state_array[0][j] = BitVector(intVal=state_array[0][j], size=8)
        state_array[1][j] = BitVector(intVal=state_array[1][j], size=8)
        state_array[2][j] = BitVector(intVal=state_array[2][j], size=8)
        state_array[3][j] = BitVector(intVal=state_array[3][j], size=8)
        # newStateArray = [[0 for x in range(4)] for x in range(4)]
        
        
        newStateArray[0][j] = (state_array[0][j].gf_multiply_modular(e_const, AES_modulus, 8)) ^ (state_array[1][j].gf_multiply_modular(b_const, AES_modulus, 8)) ^ (state_array[2][j].gf_multiply_modular(d_const, AES_modulus, 8)) ^ (state_array[3][j].gf_multiply_modular(nine_const, AES_modulus, 8))
        newStateArray[1][j]  = (state_array[0][j].gf_multiply_modular(nine_const, AES_modulus, 8)) ^ (state_array[1][j].gf_multiply_modular(e_const, AES_modulus, 8)) ^ (state_array[2][j].gf_multiply_modular(b_const, AES_modulus, 8)) ^ (state_array[3][j].gf_multiply_modular(d_const, AES_modulus, 8))
        newStateArray[2][j] = (state_array[0][j].gf_multiply_modular(d_const, AES_modulus, 8)) ^ (state_array[1][j].gf_multiply_modular(nine_const, AES_modulus, 8)) ^ (state_array[2][j].gf_multiply_modular(e_const, AES_modulus, 8)) ^ (state_array[3][j].gf_multiply_modular(b_const, AES_modulus, 8))
        newStateArray[3][j]  = (state_array[0][j].gf_multiply_modular(b_const, AES_modulus, 8)) ^ (state_array[1][j].gf_multiply_modular(d_const, AES_modulus, 8)) ^ (state_array[2][j].gf_multiply_modular(nine_const, AES_modulus, 8)) ^ (state_array[3][j].gf_multiply_modular(e_const, AES_modulus, 8))
        
        
        newStateArray[0][j] = newStateArray[0][j].intValue()
        newStateArray[1][j] = newStateArray[1][j].intValue()
        newStateArray[2][j] = newStateArray[2][j].intValue()
        newStateArray[3][j] = newStateArray[3][j].intValue()
    return newStateArray


def add_round_keys(state_array, round_keys, roundNum):
    tempbv = BitVector(size=0)
    for i in range(4):
        for j in range(4):
            tempbv += BitVector(intVal=state_array[j][i], size=8)
            # state_array[j][i] ^= round_keys[(4*(num_rounds))+j][8*i : 8*(i+1)]
    # print(BitVector(intVal=state_array[j][i], size=8).get_bitvector_in_hex(), tempbv.get_bitvector_in_hex(), round_keys[roundNum].get_bitvector_in_hex(), roundNum)
    tempbv ^= round_keys[roundNum+1]
    return tempbv

def inv_add_round_keys(state_array, round_keys, roundNum):
    tempbv = BitVector(size=0)
    for i in range(4):
        for j in range(4):
            tempbv += BitVector(intVal=state_array[j][i], size=8)
            # state_array[j][i] ^= round_keys[(4*(num_rounds))+j][8*i : 8*(i+1)]
    # print(BitVector(intVal=state_array[j][i], size=8).get_bitvector_in_hex(), tempbv.get_bitvector_in_hex(), round_keys[roundNum].get_bitvector_in_hex(), roundNum)
    tempbv ^= round_keys[roundNum+1]
    return tempbv


def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant



def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

def gen_subbytes_table():
    subBytesTable = []
    
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

def get_key_from_file(filename):
    key = ""
    with open(filename) as f:
        key = f.read()
    key = key.strip()
    # key += '0' * (keysize//8 - len(key)) if len(key) < keysize//8 else key[:keysize//8]  
    key_bv = BitVector( textstring = key )
    return key_bv

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

if __name__ == "__main__":
    AES_256()
