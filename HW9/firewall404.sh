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

# Only accept packets that originate from f1.com
sudo iptables -A INPUT -p tcp --dport 80 -s f1.com -j ACCEPT

# Change source IP address to local machine IP address
sudo iptables -t nat -n -A POSTROUTING -o wlp59s0 -j MASQUERADE

# Protect against indiscriminate and nonstop scanning of ports 
sudo iptables -A FORWARD -p tcp --tcp-flags SYN,ACK,FIN,RST \
-m limit --limit 1/s -j ACCEPT

# Protect from SYN-flood attack (limit new conns to 1 per second once local machine has reached 500 requests.)
sudo iptables -A FORWARD -p tcp --syn -m limit --limit 1/s -j ACCEPT

# Allow full loopback access on your machine
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -i lo -j ACCEPT


# Port forwarding rule routing all traffic on port 8888 to port 25565
sudo iptables -t nat -A PREROUTING -p tcp -dport 8888 -j \
DNAT --to-destination :25565

# Only allows outgoing ssh connections to engineering.purdue.edu
sudo iptables -A -p tcp --dport 22 -d engineering.purdue.edu -m \
state --state NEW, ESTABLISHED -j ACCEPT

sudo iptables -A -p tcp --sport 22 -s engineering.purdue.edu -m \
state --state NEW, ESTABLISHED -j ACCEPT 

# Drop any other packets if not caught by above rules
sudo iptables -A INPUT -j DROP
sudo iptables -A FORWARD -j DROP
sudo iptables -A OUTPUT -j DROP


