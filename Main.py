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


def updateFiles(new,old):
    return None
    


def launch():
    print "launching controller..."
    oldFiles = getFiles()
    schemas = SchemaStore(oldFiles)
    schemas.printSchemas()


    
    openflow = Openflow(schemas)
    openflow.start()
    sflow = Sflow(schemas)
    sflow.start()
    monitor = Monitor(sflow,openflow,schemas)
    monitor.start()
    
    
"""putting an infinite loop in main breaks EVERYTHING. mostly pox.core.openflow compoenent registrting"""


"""
    if changedFiles is not None:
        print "updating schemas..."
        schemas = SchemaStore(changedFiles)
        openflow = Openflow(schemas)
        openflow.start()
        sflow = Sflow(schemas)
        sflow.start()
        monitor = Monitor(sflow,openflow,schemas)
        monitor.start() """
    

  
















