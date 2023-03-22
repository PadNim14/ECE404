# Flush and delete all previously defined rules and chains
sudo iptables -t filter -F
sudo iptables -t filter -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t raw -F
sudo iptables -t raw -X

# Default policy for INPUT/FORWARD/OUTPUT on filter: ACCEPT
# Change default policies for all 3 chains to REJECT
sudo iptables -P INPUT REJECT
sudo iptables -P FORWARD REJECT
sudo iptables -P OUTPUT REJECT

# For all outgoing packets, change source IP address to local machine IP
sudo iptables -t nat -A POSTROUTING --destination 128.46.4.36 -j SNAT --to-source 128.210.107.85

# Protect against nonstop scanning of ports 


# Protect from SYN-flood attack (limit new conns to 1 per second once local machine has reached 500 requests.)


# Allow full loopback access on your machine


# Port forwarding rule routing all traffic on port 8888 to port 25565


# Only allows outgoing ssh connections to engineering.purdue.edu


# Drop any other packets if not caught by above rules


