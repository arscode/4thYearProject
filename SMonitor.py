
from subprocess import call 
import httplib
import urllib
import time
import json
import requests

class SMonitor(object):


    def __init__(self, matches, switches):
        #get a list of switches, put sflow agents on all of them
        #add all of the matches into corresponding sflow flow defs and thresholds
        #go through all of the flow defs, and push them onto all of the switches.
        #switches and flows seperate. register agents on all switches, and from then on push flows to sflow-rt collector, independent of switches
        #each sflow agent needs its own ip address
        
        self.switches = switches
        self.requests = matches
        self.collectorIP = "127.0.0.1"
        self.collectorPort = "6343"
        self.sampling = "64"
        self.polling = "10"
    
     
        self.sendAllFlows()
        self.getFlow()
        #self.getAllFlows()






   
    
        



    def sendAllFlows(self):
        for r in self.requests.requests:
            keys,values,app = self.parseRequest(r)
            self.sendFlow(keys,values,app)
        
            #use javascript functions. see scripts in sflow api
            
            
            
    """poll collector to see if any of the matches have been found.
    go through all of the matches, and see if any have been completed.
    rewrite method so it takes in a specific flow, and checks it """
    def getFlow(self):
        #write timer without pausing thread
        while True:
            response = requests.get("http://localhost:8008/flows/json?name=14&maxFlows=100&timeout=60") #set flow def to log lows
            if response.status_code != 200: continue
            flows = response.json()
            if len(flows) != 0:
                flowID = flows[0]["flowID"]
                flows.reverse()
                for f in flows:
                    print str(f['flowKeys']) + ',' + str(int(f['value'])) + ',' + str(f['end'] - f['start']) + ',' + f['agent'] + ',' + str(f['dataSource'])
        


    def getAllFlows(self):
    
        
        flow = "/flows/json"
        count = 0
        while True:
           r = requests.get("http://localhost:8008"+flow)
           if r.status_code != 200: break
           events = r.json()
           print events
           eventID = events[0]["eventID"]
           for e in events:
               if 'incoming' == e['metric']:
                   r = requests.get(target + '/metric/' + e['agent'] + '/' + e['dataSource'] + '.' + e['metric'] + '/json')
                   metric = r.json()
                   if len(metric) > 0:
                        print metric[0]["topKeys"][0]["key"]

        #print attributes
    def sendFlow(self,keys,values,name):
        flow = "/flow/"+name+"/json"
        attributes = "{keys:'"
        attributes += ','.join(keys)
        attributes += "', filter:'"
        attributes += ','.join(values)
        attributes += "', log:'true"
        attributes += "',value:'frames'}"
        payload = dict([('keys:',','.join(keys)), ('filter:',','.join(values)),('value:','frames')])
        #print attributes
        #print payload.items()
       
        r = requests.put("http://localhost:8008"+flow,data=attributes)
        
        print r.text
        

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

