import re
import threading
import Queue
import os
import time


from Schema import Schema, SchemaStore
from Openflow import Openflow
from Sflow import Sflow


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


def monitor():

    schemas = SchemaStore(getFiles())
    schemas.printSchemas()

   
    
    openflow = Openflow(schemas)
    openflow.start()
    """infinite loop breaks l2 learning"""
    #while True:
     #   pass
        #print "...another 20 seconds"
    
    #sflow = Sflow(schemas)
    #sflow.start()

     # if sflow.recentMatches:
       # print sflow.recentMatches
        #for every schema:
        #check recentMatches
        #check utilisatoin
        #check latency
        #check jitter
        



monitor()


      
    


















