

# should only be one connection from host, so each host has one ip addr 

/home/james/mininet/sflow-rt/start.sh &

#configure host ip addresses. hosts should be set by --mac option
#worse comes to worse, set ip addr for a switch and use that a source of DDoS

#bridge the interaces








ovs-vsctl -- --id=@sflow create sflow agent=4_2_2-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 4_2_2  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=4_2_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 4_2_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=4_1_2-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 4_1_2  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=4_1_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 4_1_1  sflow=@sflow

ovs-vsctl -- --id=@sflow create sflow agent=3_3_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 3_3_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=3_2_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 3_2_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=3_1_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 3_1_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=3_0_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 3_0_1  sflow=@sflow

ovs-vsctl -- --id=@sflow create sflow agent=2_3_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 2_3_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=2_2_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 2_2_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=2_1_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 2_1_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=2_0_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 2_0_1  sflow=@sflow

ovs-vsctl -- --id=@sflow create sflow agent=1_3_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 1_3_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=1_2_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 1_2_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=1_1_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 1_1_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=1_0_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 1_0_1  sflow=@sflow

ovs-vsctl -- --id=@sflow create sflow agent=0_3_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 0_3_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=0_2_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 0_2_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=0_0_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 0_0_1  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=0_1_1-eth1 target=127.0.0.1 sampling=1 polling=1 -- -- set bridge 0_1_1  sflow=@sflow

