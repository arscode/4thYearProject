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


def updateFiles():
    return None
    


oldFiles = getFiles()
schemas = SchemaStore(oldFiles)
schemas.printSchemas()

"""fix parsing, get flows to work. work on architecture. make canonical topology, with ip addresses.
     switch to layer 3 routing. check latency properly, testing different maounts
      and cleearing the ARP cache. then combine flows with latency """
    
openflow = Openflow(schemas)
openflow.start()
sflow = Sflow(schemas)
sflow.start()
monitor = Monitor(sflow,openflow,schemas)
monitor.start()

while True:
    time.sleep(3000) #check every 5 mins for new schemas
    newFiles = getFiles()
    changedFiles = updateFiles(newFiles,oldFiles)
    if changedFiles:
        print "updating schemas..."
        schemas = SchemaStore(changedFiles)
        openflow = Openflow(schemas)
        openflow.start()
        sflow = Sflow(schemas)
        sflow.start()
        monitor = Monitor(sflow,openflow,schemas)
        monitor.start()
    

  
















