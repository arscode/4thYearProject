import re
import threading
import Queue
import os

import time



from Schema import Schema, SchemaStore
from Openflow import Openflow
from Sflow import Sflow
from Monitor import Monitor



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




schemas = SchemaStore(getFiles())
schemas.printSchemas()

"""fix parsing, get flows to work. work on architecture. make canonical topology, with ip addresses.
     switch to layer 3 routing. check latency properly, testing different maounts
      and cleearing the ARP cache. then combine flows with latency """
    
openflow = Openflow(schemas)
openflow.start()
sflow = Sflow(schemas)
sflow.start()
monitor = Monitor(sflow,openflow)
monitor.start()
"""another infinite loop means it needs its own thread so it doesn't stop routing"""
    

    #sflow = Sflow(schemas)
    #sflow.start()

     # if sflow.recentMatches:
       # print sflow.recentMatches

        #for every schema:
        #check recentMatches
        #check utilisatoin
        #check latency
        #check jitter
        

"""is openflow and sflow have a match, then put in main loop
        could begin with a schema in openflow or sflow, that then gets passed around and data added too
        before it is checked for 
        
        how did I do it originally with openflow matches?
        
        sflow has a list of recent matches. it goes through its flows, checks for new data and matches, and puts in
        shared memory
        
        do same with openflow - take in a list of links to measure, and thresholds. peroidically test latency. when
        theres a match, put in shared memory
        
        main loop goes through schemas and sflow recent results. if theres a match and theres no latency info reuqired,
        print
        
        if latency is required, then check openflow sutff
        
        should the shared memory variables be lists or queues? 
        to measure flows, web server
        schema needs to include values for bytes
        make a schema with two different openflow attributes, and see what the json returns
         """


      
    


















