


#place in /home/mininet - use absolute paths
#register agent on switch three

#ifconfig s1-eth1 10.0.3.1/24
#ifconfig s1-eth2 10.0.4.1/24
#ifconfig s4-eth0 10.0.3.1

ifconfig s2-eth1 10.0.2.1
ifconfig s1-eth1 10.0.2.3

#have added bridge
#ovs-vsctl -- '--id=@sflow' create sflow agent=eth1 target=\"127.0.0.1:6343\" sampling=10 polling=10 -- -- set bridge s2 sflow=@sflow -- set bridge s1 sflow=@sflow
ovs-vsctl -- '--id=@sflow' create sflow agent=eth0 target=\"127.0.0.1:6343\" sampling=10 polling=10 -- -- set bridge s4 sflow=@sflow -- set bridge s3 sflow=@sflow
ovs-vsctl -- '--id=@sflow' create sflow agent=s2-eth1 target=\"127.0.0.1:6343\" sampling=10 polling=10 -- -- set bridge s2 sflow=@sflow
ovs-vsctl -- '--id=@sflow' create sflow agent=s1-eth1 target=\"127.0.0.1:6343\" sampling=10 polling=10 -- -- set bridge s1 sflow=@sflow



/home/james/mininet/sflow-rt/start.sh &
#firefox http://localhost:8008 &
POX="pox"


/home/james/pox/pox.py Main Monitor nicira --convert-packet-in l2_learning  log --no-default &

curl -H "Content-Type:application/json" -X PUT --data "{keys:'ipsource,ipdestination,tcpsourceport,tcpdestinationport',value:'bytes'}" http://127.0.0.1:8008/flow/test/json
#mn '--mac' '--controller=remote' '--custom=/home/mininet/mininet/custom/diamondTopo.py' '--topo mytopo' '--switch=ovsk' 


curl -H "Content-Type:application/json" -X PUT --data "{keys:'inputifindex,outputifindex',value:'frames',filter='ipsource=10.0.0.1&ipdestination=10.0.0.2'}" http://127.0.0.1:8008/flow/trace/json

#set up flow monitoring traffic to switch 1
curl -H "Content-Type:application/json" -X PUT --data "{keys:'macdestination',value:'frames',filter='macdestination=10.0.2.3'}" http://localhost:8008/flow/s1traffic/json
#define threshold of 30k bytes


































