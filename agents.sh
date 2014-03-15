

# should only be one connection from host, so each host has one ip addr 

/home/james/mininet/sflow-rt/start.sh &

#configure host ip addresses. hosts should be set by --mac option
#worse comes to worse, set ip addr for a switch and use that a source of DDoS

ifconfig 0_0_2-eth0 0.0.0.2 netmask 255.255.255.0
ifconfig 0_0_3-eth0 0.0.0.3 netmask 255.255.255.0
ifconfig 0_1_2-eth0 0.0.1.2 netmask 255.255.255.0
ifconfig 0_1_3-eth0 0.0.1.3 netmask 255.255.255.0



ifconfig 0_0_1-eth1 0.0.0.1 netmask 255.255.255.0


ovs-vsctl -- --id=@sflow create sflow agent=0_0_1-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 0_0_1 sflow=@sflow -- set bridge 0_1_1 sflow=@sflow -- set bridge 1_0_1 sflow=@sflow -- set bridge 1_1_1 sflow=@sflow
