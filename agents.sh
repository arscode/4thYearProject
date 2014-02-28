


/home/james/mininet/sflow-rt/start.sh &



ovs-vsctl -- --id=@sflow create sflow agent=eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 0_0_1 sflow=@sflow -- set bridge 0_1_1 sflow=@sflow -- set bridge 1_0_1 sflow=@sflow -- set bridge 1_1_1 sflow=@sflow
