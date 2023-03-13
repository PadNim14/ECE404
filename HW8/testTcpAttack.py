from TcpAttack import *

if __name__ == "__main__":
    # spoofIP = '127.0.0.2' ; targetIP = '127.0.0.1'
    spoofIP = '127.0.0.4'
    targetIP = '127.0.0.1'
    rangeStart = 1 
    rangeEnd = 1024
    port = 22
    Tcp = TcpAttack(spoofIP, targetIP)
    Tcp.scanTarget(rangeStart, rangeEnd)
    if Tcp.attackTarget(port, 10):
        print('port was open to attack')
