
import threading
import time

"""in own thread, so it doesn't stop routing"""
class Monitor(threading.Thread):
    
    
    def __init__(self,sflow,openflow,schemas):
        self.sflow = sflow
        self.openflow = openflow
        threading.Thread.__init__(self)
        self.schemas = schemas.schemas
        
        

    def run(self):
        while True:
            time.sleep(5)
           
            for schema in self.schemas:
                if schema.openflow:
                    """if it has sflow attributes, and there not in recent matches, there wasn't a match
                    might have to loop through and use equals method"""
                    match = False
                    print "has sflow items"
                    for s in self.sflow.recentMatches:
                        if  s.equals(schema):
                            match = True
                    if not match: #no results from sflow stuff
                        continue
                    print "sflow match"
                
                if schema.latency: #has latency info but not match, return
                    if schema.latency[0] not in self.openflow.results:
                        continue
                    else: #if the type is 1, wanting more , and the results are ther
                        if(schema.latency[2]==1) and  not (self.openflow.results[schema.latency[0]] > schema.latency[1]):
                            continue
                
                """if code gets here, schema has matched."""
                print "notify application ",schema.application
                print schema
                    
                
             
            
        
    

