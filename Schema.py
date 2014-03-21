


from lxml import etree
from pox.core import core
import pox.openflow.libopenflow_01 as of

class Schema:
    
    
    openflowAttributes = ('Bytes','IngressPort','EthernetSource','EthernetDestination','EthernetType','VLANpriority','IPSourceAddress','IPDestinationAddress','IPprotocol','IPToS','sourcePort','destinationPort','VLANID')


    #ip protocol numbers http://en.wikipedia.org/wiki/List_of_IP_protocol_numbers

    def __init__(self):
        self.flow = dict.fromkeys(['Bytes','IngressPort','EthernetSource','EthernetDestination','EthernetType','VLANpriority','IPSourceAddress','IPDestinationAddress','IPprotocol','IPToS','sourcePort','destinationPort','VLANID'])
        self.application = None
        self.ddos = None
        self.links = [] # tuple with link tuple, and latency value
        self.latency = ()

        #self.map = {""}
     

       

        


    def fromFile(self,f):
        XMLSchema=None #try commenting this out
        with open("FlowSchema.xml") as s:
            XMLSchema = etree.parse(s)
        XMLSchema = etree.XMLSchema(XMLSchema)
        parser = etree.XMLParser(schema = XMLSchema)
        tree = etree.parse(f,parser)

        for ofattribute in Schema.openflowAttributes:
            path = '/request/openflow/'+ofattribute
            element = tree.xpath(path)
            if element:
                self.flow[ofattribute] = (element[0].text).strip()
        #convert types that shouldn't be strings. or use library to get int not text?s

        if self.flow['destinationPort']:
            self.flow['destinationPort'] = int(self.openflow['destinationPort'])

        self.application = (tree.xpath("application")[0].text).strip()
        
        if tree.xpath("latency"):
            firstMac = (tree.xpath("latency/firstMac")[0].text).strip()
            secondMac = (tree.xpath('latency/secondMac')[0].text).strip()
            time = int (tree.xpath('latency/milliseconds')[0].text)
            type = int (tree.xpath('latency/moreOrLess')[0].text)
            self.latency = ((firstMac,secondMac),time,type)

        if tree.xpath("DDoSmitigation"):
            self.ddos= int (tree.xpath("DDoSmitigation")[0].text)


    def fromPacket(self, packet):
        
        ip = packet.find('ipv4')
        if ip:
            self.flow["IPSourceAddress"]=ip.srcip
            self.flow["IPDestinationAddress"]=ip.dstip
            self.flow["IPToS"]=ip.tos
            self.flow["IPprotocol"]=ip.protocol
        
        ether = packet.find('ethernet')
        if ether:
            self.flow["EthernetSource"]=ether.src
            self.flow["EthernetDestination"]=ether.dst
            self.flow["EthernetType"]=ether.type
        tcp = packet.find('tcp')
        if tcp:
            self.flow["sourcePort"] = tcp.srcport
            self.flow["destinationPort"] = tcp.dstport
        udp = packet.find('udp')
        if udp:    
            self.flow["sourcePort"] = udp.srcport
            self.flow["destinationPort"] = udp.dstport
        self.application = "switch response"


    def fromJSON(self,data,schema):
        
        """for key, value in data[0].iteritems():"""

        print data
        value = data[0]["key"]
      
        if type(value)=='unicode':
            value = value.encode('utf-8')

            
        for attribute in schema.flow:
            if schema.flow[attribute] != None:
                self.flow[attribute] = value

        print "-------"
        for attribute in self.flow:
            print attribute,self.flow[attribute]

        print "-------"
            #if value.isdigit(): 
            #self.flow['destinationPort'] = float(value) 

        #get key, find right openflow bit, put value in
        #print keys
        
        #return schema

        


        #original schema will be a subset of the packet attributes
    def equalsFlow(self,otherSchema):
        for attribute,value in self.flow.items():
            if otherSchema.flow[attribute] != value:
                return False
        return True

  

class SchemaStore:
    schemas = []

    def __init__(self,xmlFiles):
        for xmlFile in xmlFiles:
            schema = Schema()
            schema.fromFile(xmlFile)
            self.schemas += [schema]
                
    def printSchemas(self):
        for r in self.schemas:
            print r.application
            print r.openflow.items()
            print r.latency

        def check(self,originalSchema, packetSchema):
            print "original attributes are "
            print originalSchema.openflow.keys()

            print "other request attributes"
            print packetSchema.openflow.keys()

            print "checking..."
        
	   
            for r in self.schemas:
                r.equals(schema)
        

