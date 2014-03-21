
import threading
import time
from DDoSPrevention import DDoSPrevention

"""in own thread, so it doesn't stop routing"""
class Monitor(threading.Thread):
    
    
    def __init__(self,sflow,openflow,lowestThreshold,schemas):
        self.sflow = sflow
        self.openflow = openflow
        self.schemas = schemas
        self.colours = {"RED":"\033[1m\033[31m","WHITE":"\033[1m\033[37m","GREEN":"\033[1m\033[32m","END":"\033[0m"}
        if lowestThreshold != 9999999:
            print self.colours["WHITE"]+" DDoS mitigation enabled with threshold "+str(lowestThreshold)+"."+self.colours["END"]
            print "\n\n"
        dos = DDoSPrevention(lowestThreshold)
        dos.start()
        threading.Thread.__init__(self)

        


        
        
    def run(self):
        while True:
            time.sleep(10) #give everything time to measure
            

            for schema in self.schemas:
                if schema.flow:
                    #print self.sflow.recentMatches 
                    for flowSchema in self.sflow.recentMatches:
                        if schema.equalsFlow(flowSchema):
                            print self.colours["GREEN"]+"flow detected that has matched schema "+str(schema.application)+"."
                            attributes = "Matched flow: "
                            for attribute in schema.flow:
                                if attribute is not None:
                                    attributes+= str(attribute)+":"+str(schema.flow[attribute])
                            print attributes
                            print "\n"

                
              
                if schema.latency:
                    link = schema.latency[0]
                    if link in self.openflow.results.keys():
                        print self.colours["WHITE"]+"switches "+str(link)+" have latency "+str(self.openflow.results[link]*1000)+" milliseconds."+self.colours["END"]
                        print self.colours["RED"]+" Exceeded threshold of "+str(schema.latency[1])+"."+self.colours["END"]
                        print "\n"
            

