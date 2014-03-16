

# should only be one connection from host, so each host has one ip addr 

/home/james/mininet/sflow-rt/start.sh &

#configure host ip addresses. hosts should be set by --mac option
#worse comes to worse, set ip addr for a switch and use that a source of DDoS

#bridge the interaces








ovs-vsctl -- --id=@sflow create sflow agent=0_0_2-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 0_0_2  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=0_0_3-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 0_0_3  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=0_1_2-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 0_1_2  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=0_1_3-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 0_1_3  sflow=@sflow

ovs-vsctl -- --id=@sflow create sflow agent=1_0_2-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 1_0_2  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=1_0_3-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 1_0_3  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=1_1_2-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 1_1_2  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=1_1_3-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 1_1_3  sflow=@sflow

ovs-vsctl -- --id=@sflow create sflow agent=2_0_2-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 2_0_2  sflow=@sflow
ovs-vsctl -- --id=@sflow create sflow agent=2_0_3-eth1 target=127.0.0.1 sampling=10 polling=20 -- -- set bridge 2_0_3  sflow=@sflow