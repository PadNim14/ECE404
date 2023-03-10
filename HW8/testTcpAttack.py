from TcpAttack import *

spoofIP = '10.1.1.1' ; targetIP = '10.1.1.2'
rangeStart = int ; rangeEnd = int; port = int
Tcp = TcpAttack(spoofIP, targetIP)
Tcp.scanTarget(rangeStart, rangeEnd)
if Tcp.attackTarget(port, 10):
    print('port was open to attack')
