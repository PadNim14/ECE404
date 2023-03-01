# Homework Number: 6
# Name: Nimal Padmanabhan
# ECN Login: npadmana   
# Due Date: 2/28/23

from BitVector import *
import sys
import random
from solve_pRoot import solve_pRoot
e = 3

class PrimeGenerator( object ):                                              #(A1)

    def __init__( self, **kwargs ):                                          #(A2)
        bits = debug = None                                                  #(A3)
        if 'bits' in kwargs  :     bits = kwargs.pop('bits')                 #(A4)
        if 'debug' in kwargs :     debug = kwargs.pop('debug')               #(A5)
        self.bits            =     bits                                      #(A6)
        self.debug           =     debug                                     #(A7)
        self._largest        =     (1 << bits) - 1                           #(A8)

    def set_initial_candidate(self):                                         #(B1)
        candidate = random.getrandbits( self.bits )                          #(B2)
        if candidate & 1 == 0: candidate += 1                                #(B3)
        candidate |= (1 << self.bits-1)                                      #(B4)
        candidate |= (2 << self.bits-3)                                      #(B5)
        self.candidate = candidate                                           #(B6)

    def set_probes(self):                                                    #(C1)
        self.probes = [2,3,5,7,11,13,17]                                     #(C2)

    # This is the same primality testing function as shown earlier
    # in Section 11.5.6 of Lecture 11:
    def test_candidate_for_prime(self):                                      #(D1)
        'returns the probability if candidate is prime with high probability'
        p = self.candidate                                                   #(D2)
        if p == 1: return 0                                                  #(D3)
        if p in self.probes:                                                 #(D4)
            self.probability_of_prime = 1                                    #(D5)
            return 1                                                         #(D6)
        if any([p % a == 0 for a in self.probes]): return 0                  #(D7)
        k, q = 0, self.candidate-1                                           #(D8)
        while not q&1:                                                       #(D9)
            q >>= 1                                                          #(D10)
            k += 1                                                           #(D11)
        if self.debug: print("q = %d  k = %d" % (q,k))                       #(D12)
        for a in self.probes:                                                #(D13)
            a_raised_to_q = pow(a, q, p)                                     #(D14)
            if a_raised_to_q == 1 or a_raised_to_q == p-1: continue          #(D15)
            a_raised_to_jq = a_raised_to_q                                   #(D16)
            primeflag = 0                                                    #(D17)
            for j in range(k-1):                                             #(D18)
                a_raised_to_jq = pow(a_raised_to_jq, 2, p)                   #(D19)
                if a_raised_to_jq == p-1:                                    #(D20)
                    primeflag = 1                                            #(D21)
                    break                                                    #(D22)
            if not primeflag: return 0                                       #(D23)
        self.probability_of_prime = 1 - 1.0/(4 ** len(self.probes))          #(D24)
        return self.probability_of_prime                                     #(D25)

    def findPrime(self):                                                     #(E1)
        self.set_initial_candidate()                                         #(E2)
        if self.debug:  print("    candidate is: %d" % self.candidate)       #(E3)
        self.set_probes()                                                    #(E4)
        if self.debug:  print("    The probes are: %s" % str(self.probes))   #(E5)
        max_reached = 0                                                      #(E6)
        while 1:                                                             #(E7)
            if self.test_candidate_for_prime():                              #(E8)
                if self.debug:                                               #(E9)
                    print("Prime number: %d with probability %f\n" %       
                          (self.candidate, self.probability_of_prime) )      #(E10)
                break                                                        #(E11)
            else:                                                            #(E12)
                if max_reached:                                              #(E13)
                    self.candidate -= 2                                      #(E14)
                elif self.candidate >= self._largest - 2:                    #(E15)
                    max_reached = 1                                          #(E16)
                    self.candidate -= 2                                      #(E17)
                else:                                                        #(E18)
                    self.candidate += 2                                      #(E19)
                if self.debug:                                               #(E20)
                    print("    candidate is: %d" % self.candidate)           #(E21)
        return self.candidate                                                #(E22)
        

def break_rsa():
    tag = sys.argv[1]
    if tag == '-e':
        message_file = sys.argv[2]
        enc1 = sys.argv[3]
        enc2 = sys.argv[4]
        enc3 = sys.argv[5]
        n_1_2_3 = sys.argv[6]
        break_rsa_encrypt(message_file, enc1, enc2, enc3, n_1_2_3)
    
    elif tag == '-c':
        enc1 = sys.argv[2]
        enc2 = sys.argv[3]
        enc3 = sys.argv[4]
        n_1_2_3 = sys.argv[5]
        cracked = sys.argv[6]
        break_rsa_cracked(enc1, enc2, enc3, n_1_2_3, cracked)
        # rsa_encrypt(message_file, p_text, q_text, encrypted_file)
    else:
        print("Invalid tags. Valid tags: -e, -c")
        
def rsa_key_gen():
    # Generate two different primes p and q
    # POUT = open(p_text, 'w')
    # QOUT = open(q_text, 'w')
    temp_bv1 = BitVector(intVal=0, size=128)
    temp_bv2 = BitVector(intVal=0, size=128)
    gen = PrimeGenerator(bits=128)
    p = 0
    q = 0
    while p == q:
        # Generate prime p
        p = gen.findPrime()
        temp_bv1.set_value(intVal=p)
        # getting p - 1 value
        p_1 = p - 1
        e_temp = e
        # gcd
        while e_temp:
            p_1 = e_temp
            e_temp = p_1 % e_temp
        
        while not(temp_bv1[0] and temp_bv1[1]) and e_temp != 1:
            p = gen.findPrime()
            temp_bv1.set_value(intVal=p)
            p_1 = p - 1
            e_temp = e
            # gcd
            while e_temp:
                p_1 = e_temp
                e_temp = p_1 % e_temp
                
        # Generate prime q
        q = gen.findPrime()
        temp_bv2.set_value(intVal=p)
        q_1 = q - 1
        e_temp2 = e
        # gcd
        while e_temp2:
            q_1 = e_temp2
            e_temp2 = q_1 % e_temp2
            
        while not(temp_bv2[0] and temp_bv2[1]) and e_temp2 != 1:
            q = gen.findPrime()
            temp_bv2.set_value(intVal=q)
            q_1 = q - 1
            e_temp2 = e
            # gcd
            while e_temp2:
                q_1 = e_temp2
                e_temp2 = q_1 % e_temp2
    
    # public: [e, n]
    # private: [d, n]
    return p, q
   
   
 

def break_rsa_encrypt(message_file, enc1, enc2, enc3, n_1_2_3):
    enc_1_OUT = open(enc1, 'w')
    enc_2_OUT = open(enc2, 'w')
    enc_3_OUT = open(enc3, 'w')
    nOUT = open(n_1_2_3, 'w')
    
    p1, q1 = rsa_key_gen()
    p2, q2 = rsa_key_gen()
    p3, q3 = rsa_key_gen()
    
    n1 = p1 * q1
    n2 = p2 * q2
    n3 = p3 * q3

    nOUT.write(str(n1) + "\n")
    nOUT.write(str(n2) + "\n")
    nOUT.write(str(n3))
            
    p1_bv = BitVector(intVal=int(p1))
    q1_bv = BitVector(intVal=int(q1))

    p2_bv = BitVector(intVal=int(p2))
    q2_bv = BitVector(intVal=int(q2))
    
    p3_bv = BitVector(intVal=int(p3))
    q3_bv = BitVector(intVal=int(q3))
    
        
     
    message_bv = BitVector(filename=message_file)
    while message_bv.more_to_read:
        temp_bv = message_bv.read_bits_from_file(128)
        if len(temp_bv) > 0:
            if len(temp_bv) != 128:
                temp_bv.pad_from_right(128 - len(temp_bv))
            
            for j in range(3):
                if j == 0:
                    prod_1 = int(q1_bv) * int(p1_bv)
                    res1 = modular_exp(int(temp_bv), e, prod_1)
                    cipher_bv_1 = BitVector(intVal=res1, size=256)
                    # print("cipher1: " + cipher_bv_1.get_bitvector_in_hex())
                    enc_1_OUT.write(cipher_bv_1.get_bitvector_in_hex())
                elif j == 1:
                    prod_2 = int(q2_bv) * int(p2_bv)
                    res2 = modular_exp(int(temp_bv), e, prod_2)
                    cipher_bv_2 = BitVector(intVal=res2, size=256)
                    # print("cipher2: " + cipher_bv_2.get_bitvector_in_hex())
                    enc_2_OUT.write(cipher_bv_2.get_bitvector_in_hex())
                elif j == 2:
                    prod_3 = int(q3_bv) * int(p3_bv)
                    res3 = modular_exp(int(temp_bv), e, prod_3)
                    cipher_bv_3 = BitVector(intVal=res3, size=256)
                    # print("cipher3: " + cipher_bv_3.get_bitvector_in_hex())
                    enc_3_OUT.write(cipher_bv_3.get_bitvector_in_hex())
    
    enc_1_OUT.close()
    enc_2_OUT.close()
    enc_3_OUT.close()
    nOUT.close()         
               

def break_rsa_cracked(enc1, enc2, enc3, n_1_2_3, cracked):
    crack_file = open(cracked , 'w')

    enc1file = open(enc1, 'r')
    enc2file = open(enc2, 'r')
    enc3file = open(enc3, 'r')
        
    enc1_str = enc1file.read()
    enc2_str = enc2file.read()
    enc3_str = enc3file.read()
    
    enc1_bv = BitVector(hexstring=enc1_str)
    enc2_bv = BitVector(hexstring=enc2_str)
    enc3_bv = BitVector(hexstring=enc3_str)

    nFile = open(n_1_2_3, 'r')

    n1 = int(nFile.readline())
    n2 = int(nFile.readline())
    n3 = int(nFile.readline())
        
    n1_bv = BitVector(intVal=n1)
    n2_bv = BitVector(intVal=n2)
    n3_bv = BitVector(intVal=n3)
    
    # Setting up the Chinese Remainder Theorem
    N = n1 * n2 * n3
    N_1 = n2 * n3
    N_2 = n1 * n3
    N_3 = n1 * n2
    # print(N_1, N_2, N_3)
    
    N1_bv = BitVector(intVal=N_1)
    N2_bv = BitVector(intVal=N_2)
    N3_bv = BitVector(intVal=N_3)

    
    # Finding all C terms using the formula C = M * mult_inv(M mod N)
    c_1 = N_1 * int(N1_bv.multiplicative_inverse(n1_bv))
    c_2 = N_2 * int(N2_bv.multiplicative_inverse(n2_bv))
    c_3 = N_3 * int(N3_bv.multiplicative_inverse(n3_bv))

    # print(c_1, c_2, c_3)

    for i in range(len(enc1_bv) // 256):
        temp_bv1 = enc1_bv[i * 256 : (i + 1) * 256]
        temp_bv2 = enc2_bv[i * 256 : (i + 1) * 256]
        temp_bv3 = enc3_bv[i * 256 : (i + 1) * 256]
        
        # temp_bv1 = BitVector(hexstring=temp_bv1)
        # temp_bv2 = BitVector(hexstring=temp_bv2)
        # temp_bv3 = BitVector(hexstring=temp_bv3)
        # print(int(temp_bv1))
        # print(int(temp_bv2))
        # print(int(temp_bv3))
        # sys.exit()
        
        # M^3 formula using Chinese Remainder Theorem    
        decrypted_temp = ((int(temp_bv1) * c_1) + (int(temp_bv2) * c_2) + (int(temp_bv3) * c_3)) 
        decrypted_temp %= int(N)
        # Bringing it back to M using solve_pRoot()
        decrypted_temp = solve_pRoot(e, decrypted_temp)
        decrypted_bv = BitVector(intVal=decrypted_temp, size=256)
        right_block = decrypted_bv[128:256]
        crack_file.write(right_block.get_bitvector_in_ascii())
       
    crack_file.close()

    
# Lecture implementation of the pow()
def modular_exp(A, B, n):
    exp_res = 1
    while B > 0:
        if B & 1:
            exp_res = (exp_res * A) % n
        B >>= 1
        A = (A * A) % n
    return exp_res


if __name__ == "__main__":
    break_rsa()