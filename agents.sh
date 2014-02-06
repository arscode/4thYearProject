


ifconfig s1-eth1 192.168.1.1 netmask 255.255.255.0
ifconfig s2-eth1 192.168.2.1 netmask 255.255.255.0
ifconfig s3-eth1 192.168.3.1 netmask 255.255.255.0




ovs-vsctl -- --id=@sflow create sflow agent=eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge s1 sflow=@sflow -- set bridge s2 sflow=@sflow -- set bridge s3 sflow=@sflow -- set bridge s4 sflow=@sflow
