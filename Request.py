


from lxml import etree
from pox.core import core
import pox.openflow.libopenflow_01 as of

class Request:
    
    
    openflowAttributes = ('IngressPort','EthernetSource','EthernetDestination','EthernetType','VLANpriority','IPSourceAddress','IPDestinationAddress','IPprotocol','IPToS','sourcePort','destinationPort','VLANID')


    #ip protocol numbers http://en.wikipedia.org/wiki/List_of_IP_protocol_numbers

    def __init__(self,storeID):
        self.openflow = {}
        self.application = None

        


    def fromFile(self,f):
        schema=None
        with open("FlowSchema.xml") as s:
            schema = etree.parse(s)
        schema = etree.XMLSchema(schema)
        parser = etree.XMLParser(schema = schema)
        tree = etree.parse(f,parser)

        for attribute in Request.openflowAttributes:
            path = '/request/openflow/'+attribute
            element = tree.xpath(path)
            if element:
                self.openflow[attribute] = (element[0].text).strip()
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

        


        #original request will be a subset of the packet attributes
    def equals(self,otherRequest):
        for attribute,value in self.openflow.items():
            if otherRequest.openflow[attribute] != value:
                return False
        return True

        #first see what tuples this request, the one from the xml, has, and match those
        #with the request from the packet. all attributes must match. PacketRequest will have
        #more tuples than neccessary, so need to check from the xml Request one


        
