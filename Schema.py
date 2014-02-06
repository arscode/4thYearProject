


from lxml import etree
from pox.core import core
import pox.openflow.libopenflow_01 as of

class Schema:
    
    
    openflowAttributes = ('IngressPort','EthernetSource','EthernetDestination','EthernetType','VLANpriority','IPSourceAddress','IPDestinationAddress','IPprotocol','IPToS','sourcePort','destinationPort','VLANID')


    #ip protocol numbers http://en.wikipedia.org/wiki/List_of_IP_protocol_numbers

    def __init__(self):
        self.openflow = {}
        self.application = None
       

        


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
                self.openflow[ofattribute] = (element[0].text).strip()
        #convert types that shouldn't be strings. or use library to get int not text?s
        if self.openflow.has_key('destinationPort'):
            self.openflow['destinationPort'] = int(self.openflow['destinationPort'])
        self.application = (tree.xpath("application")[0].text).strip()


    def fromPacket(self, packet):
        
        ip = packet.find('ipv4')
        if ip:
            self.openflow["IPSourceAddress"]=ip.srcip
            self.openflow["IPDestinationAddress"]=ip.dstip
            self.openflow["IPToS"]=ip.tos
            self.openflow["IPprotocol"]=ip.protocol
        
        ether = packet.find('ethernet')
        if ether:
            self.openflow["EthernetSource"]=ether.src
            self.openflow["EthernetDestination"]=ether.dst
            self.openflow["EthernetType"]=ether.type
        tcp = packet.find('tcp')
        if tcp:
            self.openflow["sourcePort"] = tcp.srcport
            self.openflow["destinationPort"] = tcp.dstport
        udp = packet.find('udp')
        if udp:    
            self.openflow["sourcePort"] = tcp.srcport
            self.openflow["destinationPort"] = tcp.dstport
        self.application = "switch response"


    def fromJSON(self,data):
        #strip u
        print data[0]
        for key, value in data[0].iteritems():
            print key
            print value
        #get key, find right openflow bit, put value in
        #print keys
        
        #return schema

        


        #original schema will be a subset of the packet attributes
    def equals(self,otherSchema):
        for attribute,value in self.openflow.items():
            if otherSchema.openflow[attribute] != value:
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

        def check(self,originalSchema, packetSchema):
            print "original attributes are "
            print originalSchema.openflow.keys()

            print "other request attributes"
            print packetSchema.openflow.keys()

            print "checking..."
        
	   
            for r in self.schemas:
                r.equals(schema)
        

