import re
import threading
import Queue
import os
import time

from pox.core import core



from Schema import Schema, SchemaStore
from Openflow import Openflow
from Sflow import Sflow
from Monitor import Monitor



def getFiles():
    allFiles = os.listdir(os.getcwd())
    #print "current working directory is "+os.getcwd()
    xmlFiles = []
    xmlPattern= re.compile('^.*\.(xml)$')
    for fileName in allFiles:
        m = re.match(xmlPattern,fileName)
        if m and fileName != "FlowSchema.xml":
            xmlFiles += [m.group(0)]
    #print xmlFiles
    return xmlFiles


def updateFiles(new,old):
    return None
    
class MyComponent():
    
    def __init__(self,schemas):    
        openflow = Openflow(schemas)
        openflow.start()
        sflow = Sflow(schemas)
        sflow.start()
        monitor = Monitor(sflow,openflow,schemas)
        monitor.start()

"""what is the difference between my component and a built in one? something is stopping switch 
-controller communication"""
def launch():

    import pox.samples.pretty_log
    pox.samples.pretty_log.launch()
    print "launching controller..."
    oldFiles = getFiles()
    schemas = SchemaStore(oldFiles)
    core.registerNew(MyComponent,schemas)



    
    

    

  
















