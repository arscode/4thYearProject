import re
import threading
import Queue
import os

import time



from Schema import Schema, SchemaStore
from Openflow import Openflow
from Sflow import Sflow
from Monitor import Monitor
from DDoSPrevention import DDoSPrevention



def getFiles():
    allFiles = os.listdir(os.getcwd())
    print "current working directory is "+os.getcwd()
    xmlFiles = []
    xmlPattern= re.compile('^.*\.(xml)$')
    for fileName in allFiles:
        m = re.match(xmlPattern,fileName)
        if m and fileName != "FlowSchema.xml":
            xmlFiles += [m.group(0)]
    print "\033[1m\033[37mLoaded schemas: "+str(xmlFiles)+"\033[0m"
    return xmlFiles




schemas = SchemaStore(getFiles())
"""get lowest threshold"""
lowestThreshold = 9999999
for schema in schemas.schemas:
    if schema.ddos:
        if schema.ddos<lowestThreshold:
            lowestThreshold=schema.ddos

print lowestThreshold
openflow = Openflow(schemas)
#openflow.start()
sflow = Sflow(schemas)
#sflow.start()
monitor = Monitor(None,None,lowestThreshold)
monitor.start()





