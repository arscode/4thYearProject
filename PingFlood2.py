


from os import popen
from random import randrange

interface = " 0_0_2-eth0:"
hosts = ["10.0.0.2","10.0.0.3","10.0.1.2","10.0.1.3","10.1.0.2","10.1.0.3","10.1.1.2","10.1.1.3","10.2.0.2","10.2.0.3","10.2.1.2","10.2.1.3","10.3.0.2","10.3.0.3","10.3.1.2","10.3.1.3"]


"""set up IP aliases on an interface"""
print "creating IP aliases..."
for i in range(1,200):
	args = interface+str(i)+" 10.0.100."+str(i)
	#call(["ifconfig ",args],shell=True)
	popen("ifconfig "+args)
print "done."

print "setting up reverse NAT..."
popen("iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to 10.0.200.1-10.0.200.200")
print "done."

"""ping each host 5 times. do this for all of the interfaces. should randomise this"""
print "starting attack...."
for i in range(1,200):
    alias = "10.0.100."+str(randrange(0,200))
    ping = "ping -s 1000 -c 7  -I "+alias
    
    host = hosts[randrange(len(hosts))]
    print "attacking from "+alias+" to "+host
    command = ping+" "+host
    popen(command)

print "finished."
