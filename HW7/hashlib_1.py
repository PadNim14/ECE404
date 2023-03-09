import hashlib
import sys


if __name__ == "__main__":
    INPUTFILE = open(sys.argv[1], 'r')
    OUTPUTFILE = open(sys.argv[2], 'w')
    text_buffer = INPUTFILE.readline()
    m = hashlib.sha512()
    m.update(text_buffer.encode('utf-8'))
    OUTPUTFILE.write(m.hexdigest())
    INPUTFILE.close()
    OUTPUTFILE.close()
    
    