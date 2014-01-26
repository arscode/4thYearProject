




#put request into dictionary, also update list of stuff to monitor

#when events happen, run through dictionary and see what programs want to be infinformed


from pox.core import core
import pox.openflow.libopenflow_01 as of
from Monitor import Monitor
from SMonitor import SMonitor
from Request import Request
import os
import re



class RequestStore:
    requests = []

    def __init__(self,xmlFiles):
        for xmlFile in xmlFiles:
            request = Request(xmlFile)
            request.fromFile(xmlFile)
            self.requests += [request]
                
    def printRequests(self):
        for r in self.requests:
            print r.application
            print r.openflow.items()


    def check(self,originalRequest, packetRequest):
        
        #first see what tuples this request, the one from the xml, has, and match those
        #with the request from the packet. all attributes must match. PacketRequest will have
        #more tuples than neccessary, so need to check from the xml Request one
        
        print "original attributes are "
        print originalRequest.openflow.keys()

        print "other request attributes"
        print packetRequest.openflow.keys()

        print "checking..."
        
        for r in self.requests:
            r.equals(request)
    



#put in requeststore?
def getFiles():
    allFiles = os.listdir(os.getcwd())
    print "current working directory is "+os.getcwd()
    xmlFiles = []
    xmlPattern= re.compile('^.*\.(xml)$')
    for fileName in allFiles:
        m = re.match(xmlPattern,fileName)
        if m and fileName != "FlowSchema.xml":
            xmlFiles += [m.group(0)]
    print xmlFiles
    return xmlFiles


def start_switch(event):
    Tutorial(event.connection)

            
        
def launch():    
    allRequests = RequestStore(getFiles())
    allRequests.printRequests()
    m = SMonitor(allRequests,["s1-eth1","s2-eth1","s3-eth1","s4-eth1"])

    #core.openflow.addListenerByName("ConnectionUp", start_switch)





            


