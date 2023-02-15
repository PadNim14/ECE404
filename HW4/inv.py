import copy
from BitVector import *
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


test = '23cafc6b6e826f76598263c5776f6f6f'
   

