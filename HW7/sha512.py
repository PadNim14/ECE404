# Homework Number: 7
# Name: Nimal Padmanabhan
# ECN Login: npadmana
# Due Date: 3/9/23
from BitVector import *
import sys

# Adapted from Avi Kak's SHA256.py code to fit SHA-512 algorithm.


def sha_512(inputFile, outputFile):
    FILE_IN = open(inputFile, 'r')
    FILE_OUT = open(outputFile, 'w')
    input_bv = BitVector(textstring=FILE_IN.read())
  #  The 8 32-words used for initializing the 512-bit hash buffer before we start scanning the
  #  input message block for its hashing. See page 13 (page 17 of the PDF) of the NIST standard.
  #  Note that the hash buffer consists of 8 32-bit words named h0, h1, h2, h3, h4, h5, h6, and h7.
    h0 = BitVector(hexstring='6a09e667f3bcc908')
    h1 = BitVector(hexstring="bb67ae8584caa73b")
    h2 = BitVector(hexstring="3c6ef372fe94f82b")
    h3 = BitVector(hexstring="a54ff53a5f1d36f1")
    h4 = BitVector(hexstring="510e527fade682d1")
    h5 = BitVector(hexstring="9b05688c2b3e6c1f")
    h6 = BitVector(hexstring="1f83d9abfb41bd6b")
    h7 = BitVector(hexstring="5be0cd19137e2179")

  #  The K constants (also referred to as the "round constants") are used in round-based processing
  #  of each 512-bit input message block.  There is a 32-bit constant for each of the 64 rounds.
  #  These are as provided on page 10 (page 14 of the PDF) of the NIST standard.  Note that these
  #  are ONLY USED in STEP 3 of the hashing algorithm where we take each 512-bit input message block
  #  through 64 rounds of processing.
    K_bv = [
        BitVector(hexstring="428a2f98d728ae22"),
        BitVector(hexstring="7137449123ef65cd"),
        BitVector(hexstring="b5c0fbcfec4d3b2f"),
        BitVector(hexstring="e9b5dba58189dbbc"),
        BitVector(hexstring="3956c25bf348b538"),
        BitVector(hexstring="59f111f1b605d019"),
        BitVector(hexstring="923f82a4af194f9b"),
        BitVector(hexstring="ab1c5ed5da6d8118"),
        BitVector(hexstring="d807aa98a3030242"),
        BitVector(hexstring="12835b0145706fbe"),
        BitVector(hexstring="243185be4ee4b28c"),
        BitVector(hexstring="550c7dc3d5ffb4e2"),
        BitVector(hexstring="72be5d74f27b896f"),
        BitVector(hexstring="80deb1fe3b1696b1"),
        BitVector(hexstring="9bdc06a725c71235"),
        BitVector(hexstring="c19bf174cf692694"),
        BitVector(hexstring="e49b69c19ef14ad2"),
        BitVector(hexstring="efbe4786384f25e3"),
        BitVector(hexstring="0fc19dc68b8cd5b5"),
        BitVector(hexstring="240ca1cc77ac9c65"),
        BitVector(hexstring="2de92c6f592b0275"),
        BitVector(hexstring="4a7484aa6ea6e483"),
        BitVector(hexstring="5cb0a9dcbd41fbd4"),
        BitVector(hexstring="76f988da831153b5"),
        BitVector(hexstring="983e5152ee66dfab"),
        BitVector(hexstring="a831c66d2db43210"),
        BitVector(hexstring="b00327c898fb213f"),
        BitVector(hexstring="bf597fc7beef0ee4"),
        BitVector(hexstring="c6e00bf33da88fc2"),
        BitVector(hexstring="d5a79147930aa725"),
        BitVector(hexstring="06ca6351e003826f"),
        BitVector(hexstring="142929670a0e6e70"),
        BitVector(hexstring="27b70a8546d22ffc"),
        BitVector(hexstring="2e1b21385c26c926"),
        BitVector(hexstring="4d2c6dfc5ac42aed"),
        BitVector(hexstring="53380d139d95b3df"),
        BitVector(hexstring="650a73548baf63de"),
        BitVector(hexstring="766a0abb3c77b2a8"),
        BitVector(hexstring="81c2c92e47edaee6"),
        BitVector(hexstring="92722c851482353b"),
        BitVector(hexstring="a2bfe8a14cf10364"),
        BitVector(hexstring="a81a664bbc423001"),
        BitVector(hexstring="c24b8b70d0f89791"),
        BitVector(hexstring="c76c51a30654be30"),
        BitVector(hexstring="d192e819d6ef5218"),
        BitVector(hexstring="d69906245565a910"),
        BitVector(hexstring="f40e35855771202a"),
        BitVector(hexstring="106aa07032bbd1b8"),
        BitVector(hexstring="19a4c116b8d2d0c8"),
        BitVector(hexstring="1e376c085141ab53"),
        BitVector(hexstring="2748774cdf8eeb99"),
        BitVector(hexstring="34b0bcb5e19b48a8"),
        BitVector(hexstring="391c0cb3c5c95a63"),
        BitVector(hexstring="4ed8aa4ae3418acb"),
        BitVector(hexstring="5b9cca4f7763e373"),
        BitVector(hexstring="682e6ff3d6b2b8a3"),
        BitVector(hexstring="748f82ee5defb2fc"),
        BitVector(hexstring="78a5636f43172f60"),
        BitVector(hexstring="84c87814a1f0ab72"),
        BitVector(hexstring="8cc702081a6439ec"),
        BitVector(hexstring="90befffa23631e28"),
        BitVector(hexstring="a4506cebde82bde9"),
        BitVector(hexstring="bef9a3f7b2c67915"),
        BitVector(hexstring="c67178f2e372532b"),
        BitVector(hexstring="ca273eceea26619c"),
        BitVector(hexstring="d186b8c721c0c207"),
        BitVector(hexstring="eada7dd6cde0eb1e"),
        BitVector(hexstring="f57d4f7fee6ed178"),
        BitVector(hexstring="06f067aa72176fba"),
        BitVector(hexstring="0a637dc5a2c898a6"),
        BitVector(hexstring="113f9804bef90dae"),
        BitVector(hexstring="1b710b35131c471b"),
        BitVector(hexstring="28db77f523047d84"),
        BitVector(hexstring="32caab7b40c72493"),
        BitVector(hexstring="3c9ebe0a15c9bebc"),
        BitVector(hexstring="431d67c49c100d4c"),
        BitVector(hexstring="4cc5d4becb3e42b6"),
        BitVector(hexstring="597f299cfc657e2a"),
        BitVector(hexstring="5fcb6fab3ad6faec"),
        BitVector(hexstring="6c44198c4a475817")
    ]
    '''
    STEP 1: Pad the message so that its length is an integral multiple of 1024
    bits, the block size. The only complication here is that the last 128 bits
    of the last block must contain a value that is the length of the message.
    '''
    length = input_bv.length()
    bv1 = input_bv + BitVector(bitstring="1")
    length1 = bv1.length()
  # print(length1)
    howmanyzeros = (896 - length1) % 1024
  # print(howmanyzeros)
    zerolist = [0] * howmanyzeros
    bv2 = bv1 + BitVector(bitlist=zerolist)
    bv3 = BitVector(intVal=length, size=128)
    bv4 = bv2 + bv3
  # print(bv4.length())

  # Initialize the array of "words" for storing the message schedule for a block of the input message:
    words = [None] * 80

    for n in range(0, bv4.length(), 1024):
        block = bv4[n:n+1024]

        '''
        STEP 2: Generate the message schedule required for processing a 1024-bit
        block of the input message. The message schedule consists of 80 64-bit
        words. The first 16 of these words are obtained directly from the
        1024-bit message block. The rest of the words are obtained by applying
        permutation and mixing operations to the some of the previously
        generated words.
        '''
        words[0:16] = [block[i:i+64] for i in range(0, 1024, 64)]
        # print(words)
    # print(words)
    #  Now we need to expand the first 16 32-bit words of the message schedule into a full schedule
    #  that contains 64 32-bit words. This involves using the functions sigma0 and sigma1 as shown
    #  below:
        for i in range(16, 80):
            i_minus_2_word = words[i-2]
            i_minus_15_word = words[i-15]
        #  The sigma1 function is applied to the i_minus_2_word and the sigma0 function is applied to
        #  the i_minus_15_word:
            sigma0 = (i_minus_15_word.deep_copy() >> 1) ^ (i_minus_15_word.deep_copy() >> 8) ^ \
                (i_minus_15_word.deep_copy().shift_right(7))
            sigma1 = (i_minus_2_word.deep_copy() >> 19) ^ (i_minus_2_word.deep_copy() >> 61) ^ \
                (i_minus_2_word.deep_copy().shift_right(6))
            words[i] = BitVector(intVal=(int(words[i-16]) + int(sigma1) + int(words[i-7]) +
                                         int(sigma0)) & 0xFFFFFFFFFFFFFFFF, size=64)
    #  Before we can start STEP 3, we need to store the hash buffer contents obtained from the
    #  previous input message block in the variables a,b,c,d,e,f,g,h:
  # print(words)
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        '''
        STEP 3: Apply round-based processing to each 1024-bit input message
        block. There are 80 rounds to be carried out for each message block.
        For this round-based processing, we first store the hash values
        calculated for the PREVIOUS MESSAGE BLOCK in temporary 64-bit
        variables denoted a, b, c, d, e, f, g, h. In the ith round, we permute the
        values stored in these eight variables and, with two of the variables, we
        mix in the message schedule word words[i] and a round constant K[i].
        '''
        for i in range(80):
            ch = (e & f) ^ ((~e) & g)
            maj = (a & b) ^ (a & c) ^ (b & c)
            sum_a = ((a.deep_copy()) >> 28) ^ (
                (a.deep_copy()) >> 34) ^ ((a.deep_copy()) >> 39)
            sum_e = ((e.deep_copy()) >> 14) ^ (
                (e.deep_copy()) >> 18) ^ ((e.deep_copy()) >> 41)
            # print(sum_e.get_bitvector_in_hex())
            t1 = BitVector(intVal=(int(h) + int(ch) + int(sum_e) + int(words[i]) + int(K_bv[i])) &
                           0xFFFFFFFFFFFFFFFF, size=64)
            t2 = BitVector(intVal=(int(sum_a) + int(maj))
                           & 0xFFFFFFFFFFFFFFFF, size=64)
            h = g
            g = f
            f = e
            e = BitVector(intVal=(int(d) + int(t1)) &
                          0xFFFFFFFFFFFFFFFF, size=64)
            d = c
            c = b
            b = a
            a = BitVector(intVal=(int(t1) + int(t2)) &
                          0xFFFFFFFFFFFFFFFF, size=64)

        # print((h0+h1+h2+h3+h4+h5+h6+h7).get_bitvector_in_hex())
        # sys.exit()
        # print("Made it here.")

        '''
        STEP 4: We update the hash values calculated for the PREVIOUS
        message block by adding to it the values in the temporary variables
        a, b, c, d, e, f, g, h.
        '''
        h0 = BitVector(intVal=(int(h0) + int(a)) & 0xFFFFFFFFFFFFFFFF, size=64)
        h1 = BitVector(intVal=(int(h1) + int(b)) & 0xFFFFFFFFFFFFFFFF, size=64)
        h2 = BitVector(intVal=(int(h2) + int(c)) & 0xFFFFFFFFFFFFFFFF, size=64)
        h3 = BitVector(intVal=(int(h3) + int(d)) & 0xFFFFFFFFFFFFFFFF, size=64)
        h4 = BitVector(intVal=(int(h4) + int(e)) & 0xFFFFFFFFFFFFFFFF, size=64)
        h5 = BitVector(intVal=(int(h5) + int(f)) & 0xFFFFFFFFFFFFFFFF, size=64)
        h6 = BitVector(intVal=(int(h6) + int(g)) & 0xFFFFFFFFFFFFFFFF, size=64)
        h7 = BitVector(intVal=(int(h7) + int(h)) & 0xFFFFFFFFFFFFFFFF, size=64)

        # print(h0.get_bitvector_in_hex())

    #  Concatenate the contents of the hash buffer to obtain a 512-element BitVector object:
    message_hash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    #  Get the hex representation of the binary hash value:
    hash_hex_string = message_hash.getHexStringFromBitVector()
    print(hash_hex_string)
    # sys.exit()
    FILE_OUT.write(hash_hex_string)
    FILE_OUT.close()


if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    sha_512(inputFile, outputFile)
