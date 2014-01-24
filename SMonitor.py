
from subprocess import call 
import httplib
import urllib
import time
import json

class SMonitor(object):


    def __init__(self, requests, switches):
        #get a list of switches, put sflow agents on all of them
        #add all of the requests into corresponding sflow flow defs and thresholds
        #go through all of the flow defs, and push them onto all of the switches.
        #switches and flows seperate. register agents on all switches, and from then on push flows to sflow-rt collector, independent of switches
        #each sflow agent needs its own ip address
        
        self.switches = switches
        self.requests = requests
        self.collectorIP = "127.0.0.1"
        self.collectorPort = "6343"
        self.sampling = "64"
        self.polling = "10"
    
        
        self.registerAgents()
        self.sendAllFlows()
        self.getAllFlows()






    def registerAgents(self): #need to configure ip addresses to use
            for s in self.switches:
                bridge = s[:2]
                register = "ovs-vsctl -- --id=@s create sFlow agent="+s+" target="+self.collectorIP+self.collectorPort+" polling="+self.polling+"     sampling="+self.sampling+" -- set Bridge "+bridge+" sflow=@s"
                print "bridge is " + bridge
                #print register
                call(register, shell=True)
    
        



    def sendAllFlows(self):
        for r in self.requests.requests:
            keys,values,app = self.parseRequest(r)
            self.sendFlow(keys,values,app)
        
            #use javascript functions. see scripts in sflow api


    def getAllFlows(self):
        headers = {}
        headers["Content-Type"] = "application/json"
        connection = httplib.HTTPConnection("localhost",8008) 
        
        flow = "/metrics/ALL/14/json"
        count = 0
        while True:
           
            connection.connect()
            r = connection.request("GET",flow," ",headers) #whitespace?
            response = connection.getresponse()
            #print response.status
            #print response.reason
        
            flows = json.loads(response.read())
            #print len(flows)
            if len(flows) == 0: continue

             #code from official sflow rt blog
            flowID = flows[0]["flowID"]
            flows.reverse()
            for f in flows:
                print str(f['flowKeys']) + ',' + str(int(f['value'])) + ',' + str(f['end'] - f['start']) + ',' + f['agent'] + ',' + str(f['dataSource'])



        #print attributes
    def sendFlow(self,keys,values,name):
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "*/*"
        connection = httplib.HTTPConnection("localhost",8008) 
        connection.connect() 
        flow = "/flow/"+name+"/json"
        attributes = "{keys:'"
        attributes += ','.join(keys)
        attributes += "', filter:'"
        attributes += ','.join(values)
        attributes += "',value:'frames'}"
        r = connection.request("PUT",flow, attributes,headers)
        print attributes
        response = connection.getresponse()
        print response.status
        print response.reason
        

    def parseRequest(self,request):
        keys = [] #use api web interface to get list of sflow attributes
        values = []
        #what do I actually send. a list of keys, of what to look for. but I need specific values as well. add key to keys and value to filter
        for attribute, value in request.openflow.items():
            value = str(value)
            if attribute=="IngressPort":
                pass

            elif attribute=="EthernetSource":
                keys.append("macsource")
                values.append("macsource="+value)

            elif attribute=="EthernetDestination":
                keys.append("macdestination")
                values.append("macdestination="+value)

            elif attribute=="EthernetType":
                keys.append('ethernetprotocol')
                values.append("ethernetprotocol="+value)

            elif attribute=="VLANpriority":
                keys.append('vlansourcepriority','vlandestinationpriority')
                values.append("vlansourcepriority="+value,"vlandestinationpriority="+value)

            elif attribute=="IPSourceAddress":
                keys.append('ipsource')
                values.append("ipsource="+value)

            elif attribute=="IPDestinationAddress":
                keys.append('ipdestination')
                values.append("ipdestination="+value)

            elif attribute=="IPprotocol": 
                keys.append("ipprotocol")
                values.append("ipprotocol="+value)

            elif attribute=="IPToS":
                keys.append("iptos")
                values.append("iptos="+value)

            elif attribute=="sourcePort": #no tcp flow key?
                keys.append("udpsourceport")
                values.append("udpsourceport="+value)

            elif attribute=="destinationPort":
                keys.append("udpdestinationport")
                values.append("udpdestinationport="+value)

            elif attribute=="VLANID":
                keys.append("vlansource","vlandestination")
                values.append("vlansource="+value,"vlandestination="+value)
        return keys,values,request.application

