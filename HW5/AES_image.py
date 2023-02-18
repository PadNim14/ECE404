#!/usr/bin/env python
# Homework Number: 5
# Name: Nimal Padmanabhan
# ECN Login: npadmana   
# Due Date: 2/21/23

from BitVector import *
from AES import AES_256_encrypt as encrypt, genTables

def ctr_aes_image(iv, image_file='image.ppm', out_file='enc_image.ppm', key_file='keyCTR.txt'):
    '''
    * Arguments:
    iv: 128-bit initialization vector
    image_file: input .ppm image file name
    out_file: encrypted .ppm image file name
    key_file: Filename containing encryption key (in ASCII)
    * Function Description:
    This function encrypts image_file using CTR mode AES and writes the encryption
    to out_file. No return value is required.
    '''
    cipher_block = None
    iv_list = []
    FILE = open(image_file, 'rb')
    ppmHeader0 = FILE.readline()
    ppmHeader1 = FILE.readline()
    ppmHeader2 = FILE.readline()
    
    key = None
    with open(key_file) as f:
        key = f.read()
    key = key.strip()
    ppmHeader = ppmHeader0 + ppmHeader1 + ppmHeader2
    OUT = open(out_file, 'wb')
    OUT.write(ppmHeader)
    
    bv = BitVector(rawbytes=FILE.read())
    genTables()
    # Making a list of initialization vectors
    for i in range(len(bv) // 128):
        iv = int(iv)
        iv_list.append(iv)
        iv += 1
    
    for i in range(len(iv_list)):
        iv = BitVector(intVal=iv_list[i], size=128)
        plaintext_block = bv[i * 128 : (i + 1) * 128]
        block_encyrpt = encrypt(iv, key)
        cipher_block = block_encyrpt ^ plaintext_block
        cipher_block.write_to_file(OUT)
    
    OUT.close()
    FILE.close()
    
    
if __name__ == "__main__":
    iv = BitVector(textstring='computersecurity')
    ctr_aes_image(iv, 'image.ppm', 'enc_image.ppm', 'keyCTR.txt')
    

