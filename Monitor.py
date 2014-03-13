
import threading
import time
from DDoSPrevention import DDoSPrevention

"""in own thread, so it doesn't stop routing"""
class Monitor(threading.Thread):
    
    
    def __init__(self,sflow,openflow):
        self.sflow = sflow
        self.openflow = openflow
        dos = DDoSPrevention(5)
        dos.start()
        threading.Thread.__init__(self)

        
        
    """go through openflow and sflow shared memory stuff and check for matches
       create a schema from values, and
        for every schema, go through all the openflow/sflow stuff and see if it matches everything"""
    def run(self):
        while True:
            time.sleep(5)
            
            for recentMatch in self.sflow.recentMatches:
                print recentMatch.openflow.items()
            
            print self.openflow.results
                
            #for recentLatencyMatch in self.openflow.results.keys():
               # print str(recentLatencyMatch) + " "+ str(self.openflow.results[recentLatencyMatch])
        
    

