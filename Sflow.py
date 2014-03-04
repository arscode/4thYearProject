



	
from subprocess import call 
import httplib
import urllib
import time
import json
import requests
import datetime
import threading
import time
import threading
from Schema import Schema


class Sflow(threading.Thread):
    def __init__(self,schemas):
        self.collectorIP = "127.0.0.1"
        self.collectorPort = "6343"
        self.sampling = "64"
        self.polling = "10"
        self.flows = []
        self.recentMatches = []
        self.schemas = schemas
        threading.Thread.__init__(self)
      


    def run(self):

    	while True:
            self.createFlows()
            self.pushFlows()
            self.checkFlows() 
   

    def parseSchema(self,schema):
        keys = [] 
        values = []
        for attribute, value in schema.openflow.items():
            value = str(value)

            if value=="None":
            	continue

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

                keys.append('vlansourcepriority')
                keys.append('vlandestinationpriority')
                values.append("vlansourcepriority="+value)
                values.append("vlandestinationpriority="+value)


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
                keys.append("tcpdestinationport")
                values.append("tcpdestinationport="+value)

            elif attribute=="VLANID":
                keys.append("vlansource")
                keys.append("vlandestination")
                values.append("vlansource="+value)
                values.append("vlandestination="+value)
        return keys,values,schema.application


    def createFlow(self,keys,values,name):
        url = "/flow/"+name+"/json"
        attributes = "{keys:'"
        attributes += ','.join(keys)
        attributes += "', filter:'"
        attributes += ','.join(values)
        attributes += "',value:'bytes'}"
        return (url,attributes,name)

    def createFlows(self):
        flows = []
        for s in self.schemas.schemas:
            flowData = self.parseSchema(s)
            flows.append(self.createFlow(flowData[0],flowData[1],flowData[2]))
        self.flows = flows



    def pushFlows(self):
        for f in self.flows:
            url = f[0]
            payload = f[1]
            connection = httplib.HTTPConnection("localhost",8008)
            connection.request("PUT",url,payload)
	    response = connection.getresponse()
            

     
    def getFlow(self,name):
        agent = "ALL"	
        url = "/activeflows/"+agent+"/"+name+"/json" #check log instead
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("GET",url," ")
        response = connection.getresponse()
        return json.loads(response.read())
     




    def checkFlows(self):
         time.sleep(10)
         for f in self.flows:
            result = self.getFlow(f[2])
            
            if result:
                schema = Schema()
                schema.fromJSON(result)
                
                for original in self.schemas.schemas:
                    if original.equals(schema):
                        self.recentMatches.append(schema)
            
        
       

   
            
            
            
 









    


