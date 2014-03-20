
import threading
import time
from DDoSPrevention import DDoSPrevention

"""in own thread, so it doesn't stop routing"""
class Monitor(threading.Thread):
    
    
    def __init__(self,sflow,openflow,lowestThreshold):
        self.sflow = sflow
        self.openflow = openflow
        
        print "lowestThreshold is ", str(lowestThreshold)
        dos = DDoSPrevention(lowestThreshold)
        dos.start()
        threading.Thread.__init__(self)

        


        
        
    def run(self):
        while True:
            time.sleep(5)
            
            #for recentMatch in self.sflow.recentMatches:
                #print recentMatch.openflow.items()
                #pass
            
            #print self.openflow.results
                
            #for recentLatencyMatch in self.openflow.results.keys():
               # print str(recentLatencyMatch) + " "+ str(self.openflow.results[recentLatencyMatch])
        
    

