
import threading
import time

"""in own thread, so it doesn't stop routing"""
class Monitor(threading.Thread):
    
    
    def __init__(self,sflow,openflow):
        self.sflow = sflow
        self.openflow = openflow
        threading.Thread.__init__(self)
        
        
    """go through openflow and sflow shared memory stuff and check for matches"""
    def run(self):
        while True:
            time.sleep(5)
            for recentMatch in self.sflow.recentMatches:
                print recentMatch.openflow.items()
        
    

