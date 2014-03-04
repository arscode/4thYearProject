"""takes in a threshold, defines a flow to monitor it, defines threshold, periodically polls
   if threshold exceeded, time stamp and block ip. later on, unblock ips again"""

class DDoSPrevention:
    
    
    def __init__(self,threshold):
        self.pushMonitoringFlow()
        self.pushThreshold(threshold)
        self.monitor()
        
        
        
        
    def pushMonitoringFlow(self):
        url = "/flow/ddos/json"
        payload = "{keys:'ipsource,ipdestination', value:'frames'}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
    
    
    
    def pushThreshold(self,threshold):
        url = "/threshold/ddos/json"
        payload = "{metric:'ddos',value:"+threshold+"}"
        connection = httplib.HTTPConnection("localhost",8008)
        connection.request("PUT",url,payload)
        return connection.getresponse() #do error checking
        
        
    


   
   
   