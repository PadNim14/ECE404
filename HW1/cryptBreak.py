#!/usr/bin/env python
# Homework Number: 1
# Name: Nimal Padmanabhan
# ECN Login: npadmana   
# Due Date: 1/19/23

# This code was adapted from the lecture slides.
from BitVector import *

def cryptBreak(ciphertextFile, key_bv):
    # Arguments:
    # * ciphertextFile: String containing file name of the ciphertext
    # * key_bv: 16-bit BitVector for the decryption key
    #
    # Function Description:
    # Attempts to decrypt the ciphertext within ciphertextFile file using
    # key_bv and returns the original plaintext as a string

    PassPhrase = "Hopes and dreams of a million years"                          #(C)

    BLOCKSIZE = 16                                                              #(D)
    numbytes = BLOCKSIZE // 8                                                   #(E)

    # Reduce the passphrase to a bit array of size BLOCKSIZE:
    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
    for i in range(0,len(PassPhrase) // numbytes):                              #(G)
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
        bv_iv ^= BitVector( textstring = textstr )                              #(I)

    # Create a bitvector from the ciphertext hex string:
    FILEIN = open(ciphertextFile)                                                  #(J)
    encrypted_bv = BitVector( hexstring = FILEIN.read() )                       #(K)
    '''
    for i in range(pow(2, BLOCKSIZE)):
        key = '{0:016b}'.format(i)
        print(key)
        key_bv = BitVector(intVal=i, size=BLOCKSIZE)                               #(P)
    '''  
       
        # Create a bitvector for storing the decrypted plaintext bit array: 
    msg_decrypted_bv = BitVector( size = 0 )                                    #(T)

    # Carry out differential XORing of bit blocks and decryption:   
    previous_decrypted_block = bv_iv                                            #(U)
    for j in range(0, len(encrypted_bv) // BLOCKSIZE):                          #(V)
        bv = encrypted_bv[j*BLOCKSIZE:(j+1)*BLOCKSIZE]                          #(W)
        temp = bv.deep_copy()                                                   #(X)
        bv ^=  previous_decrypted_block                                         #(Y)
        previous_decrypted_block = temp                                         #(Z)
        bv ^=  key_bv                                                           #(a)
        msg_decrypted_bv += bv                                                  #(b)

    # Extract plaintext from the decrypted bitvector:    
    outputtext = msg_decrypted_bv.get_text_from_bitvector()     
    '''
    print("Output Text: " + outputtext)
    # Write plaintext to the output file:
    FILEOUT = open("output.txt", 'w')                                            #(d)
    FILEOUT.write(outputtext)                                                   #(e)
    FILEOUT.close()
    '''
    return outputtext
                                                              
    
if __name__ == "__main__":
    # someRandomInteger = 9999
    # key_bv = BitVector(intVal=someRandomInteger, size=16)
    # decryptedMessage = cryptBreak('ciphertext.txt', key_bv)
    for i in range(4000, pow(2, 16)):
        # key = '{0:016b}'.format(i)
        # print(key)
        # key_bv = BitVector(intVal=i, size=16)
        print(i)
        key_bv = BitVector(intVal=i, size=16)
        decryptedMessage = cryptBreak('ciphertext.txt', key_bv)
   
        if 'Sir Lewis' in decryptedMessage:
            # print("key_bv: " + str(key_bv))
            print('Encryption broken!')
            print(decryptedMessage)
            break
        else:
            # print("key_bv: " + str(key_bv))
            print('Not decrypted yet!')
    
# 4040 (Decimal key)
# Sir Lewis Carl Davidson Hamilton (born 7 January 1985) is a British racing driver currently competing in Formula One, driving for Mercedes-AMG Petronas Formula One Team. In Formula One, Hamilton has won a joint-record seven World Drivers' Championship titles (tied with Michael Schumacher), and holds the records for the most wins (103), pole positions (103), and podium finishes (191), among many others. Statistically considered as the most successful driver in Formula One history.