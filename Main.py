




#load xml file, turn into request

#put request into dictionary, also update list of stuff to monitor

#when events happen, run through dictionary and see what programs want to be infinformed

#use SAX, no need for to hold everything in memory

from lxml import etree
Openflow = ('IngressPort','EthernetSource','EthernetDestination','EthernetType','VLANpriority','IPSourceAddress','IPDestinationAddress','IPprotocol','IPToS','sourcePort','destinationPort','VLANID')

class Request:
	openflow = {}

	def __init__(self, f):
		schema=None
		with open("FlowSchema.xml") as s:
			schema = etree.parse(s)
		schema = etree.XMLSchema(schema)
		parser = etree.XMLParser(schema = schema)
		tree = etree.parse(f,parser)

		for x in Openflow:
			element = tree.xpath(x)
			if element:
				self.openflow[x] = element[0].text
		



newRequest = Request("data.xml")
for j in newRequest.openflow.items():
	print j
