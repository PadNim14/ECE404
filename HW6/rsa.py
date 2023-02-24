# Homework Number: 5
# Name: Nimal Padmanabhan
# ECN Login: npadmana   
# Due Date: 2/28/23

from BitVector import *
import sys
import random
e = 65537


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


def get_message_from_file(filename):
    message = ""
    with open(filename) as f:
        message = f.read()
    return message
        

def rsa():
    tag = sys.argv[1]
    if tag == '-g':
        p_text = sys.argv[2]
        q_text = sys.argv[3]
        rsa_key_gen(p_text, q_text)
    
    elif tag == '-e':
        message_file = sys.argv[2]
        p_text = sys.argv[3]
        q_text = sys.argv[4]
        encrypted_file = sys.argv[5]
        rsa_encrypt(message_file, p_text, q_text, encrypted_file)
    
    elif tag == '-d':
        encrypted_file = sys.argv[2]
        p_text = sys.argv[3]
        q_text = sys.argv[4]
        decrypted_file = sys.argv[5]
        rsa_decrypt(encrypted_file, p_text, q_text, decrypted_file)
    else:
        print("Invalid tags. Valid tags: -g , -e , -d")
        

def rsa_key_gen(p_text, q_text):
    # Generate two different primes p and q
    POUT = open(p_text, 'w')
    QOUT = open(q_text, 'w')
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
        while e_temp:
            p_1 = e_temp
            e_temp = p_1 % e_temp
        
        while not(temp_bv1[0] and temp_bv1[1]) and e_temp != 1:
            p = gen.findPrime()
            temp_bv1.set_value(intVal=p)
            p_1 = p - 1
            e_temp = e
            while e_temp:
                p_1 = e_temp
                e_temp = p_1 % e_temp
                
        # Generate prime q
        q = gen.findPrime()
        temp_bv2.set_value(intVal=p)
        q_1 = q - 1
        e_temp2 = e
        while e_temp2:
            q_1 = e_temp2
            e_temp2 = q_1 % e_temp2
            
        while not(temp_bv2[0] and temp_bv2[1]) and e_temp2 != 1:
            q = gen.findPrime()
            temp_bv2.set_value(intVal=q)
            q_1 = q - 1
            e_temp2 = e
            
            while e_temp2:
                q_1 = e_temp2
                e_temp2 = q_1 % e_temp2
    
    # public: [e, n]
    # private: [d, n]
    POUT.write(str(p))
    QOUT.write(str(q))
    POUT.close()
    QOUT.close()

def rsa_encrypt(message_file, p_text, q_text, encrypted_file):
    OUT = open(encrypted_file, 'w')
    p = None
    with open(p_text) as f:
        p = f.read()
    q = None
    with open(q_text) as f:
        q = f.read()
    p_bitvec = BitVector(intVal=int(p))
    q_bitvec = BitVector(intVal=int(q))
    
    message_bv = BitVector(filename=message_file)
    while message_bv.more_to_read:
        temp_bv = message_bv.read_bits_from_file(128)
        if len(temp_bv) > 0:
            if len(temp_bv) != 128:
                temp_bv.pad_from_right(128 - len(temp_bv))
            # Insert exponentiation function
            prod_of_p_q = int(q_bitvec) * int(p_bitvec)
            res = modular_exp(int(temp_bv), e, prod_of_p_q)
            cipher_bv = BitVector(intVal=res, size=256)
            OUT.write(cipher_bv.get_bitvector_in_hex())
    OUT.close()          
               

def rsa_decrypt(encrypted_file, p_text, q_text, decrypted_file):
    encrpyted_hex = open(encrypted_file, 'r')
    cipher_bv = BitVector(hexstring=encrpyted_hex.read())
    OUT = open(decrypted_file, 'w')
    p = None
    with open(p_text) as f:
        p = f.read()
    q = None
    with open(q_text) as f:
        q = f.read()
        
    # Setting up CRT coefficients    
    p_bitvec = BitVector(intVal=int(p))
    q_bitvec = BitVector(intVal=int(q))
    n_bitvec = BitVector(intVal=(int(p) * int(q)))
    totient = BitVector(intVal=((int(p) - 1) * (int(q) - 1)))
    e_bitvec = BitVector(intVal=e, size=128)
    d_bitvec = e_bitvec.multiplicative_inverse(totient)
    # Xp = q × (inv(q) mod p)
    # Xq = p × (inv(p) mod q)
    
    x_p = int(q_bitvec) * int(q_bitvec.multiplicative_inverse(p_bitvec))
    x_q = int(p_bitvec) * int(p_bitvec.multiplicative_inverse(q_bitvec))
    for i in range(len(cipher_bv) // 256):
        temp_bv = cipher_bv[i * 256 : (i + 1) * 256]
        # Vp = C^d mod p
        #Vq = C^d mod q
        v_p = modular_exp(int(temp_bv), int(d_bitvec), int(p_bitvec))
        v_q = modular_exp(int(temp_bv), int(d_bitvec), int(q_bitvec))
        # print(v_p)
        # print(v_q)
        #C^d mod n = (VpXp + VqXq) mod n
        decrypted_temp = ((v_p * x_p) + (v_q * x_q)) % int(n_bitvec)
        # print(decrypted_temp)
        # print(len(str(decrypted_bv)))
        decrypted_bv = BitVector(intVal=decrypted_temp, size=128)
        OUT.write(decrypted_bv.get_bitvector_in_ascii())
    OUT.close()                    


def modular_exp(A, B, n):
    exp_res = 1
    while B > 0:
        if B & 1:
            exp_res = (exp_res * A) % n
        B >>= 1
        A = (A * A) % n
    return exp_res




if __name__ == "__main__":
    rsa()