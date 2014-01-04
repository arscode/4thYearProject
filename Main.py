

#strip whitespace



#load xml file, turn into request

#put request into dictionary, also update list of stuff to monitor

#when events happen, run through dictionary and see what programs want to be infinformed

#use SAX, no need for to hold everything in memory

from lxml import etree
import os
import re
Openflow = ('IngressPort','EthernetSource','EthernetDestination','EthernetType','VLANpriority','IPSourceAddress','IPDestinationAddress','IPprotocol','IPToS','sourcePort','destinationPort','VLANID')

class Request:
	openflow = {}
	application = None

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
		self.application = tree.xpath("application")[0].text


class RequestStore:
	requests = {}

	def __init__(self):
		pass

	def searchRequests():
		pass
	


newRequest = Request("data.xml")
for j in newRequest.openflow.items():
	print j
print "application is "+ newRequest.application


def getFiles():
	allFiles = os.listdir(os.getcwd())
	xmlFiles = []
	xmlPattern= re.compile('^.*\.(xml)$')
	for fileName in allFiles:
		m = re.match(xmlPattern,fileName)
		if m and fileName != "FlowSchema.xml":
			xmlFiles += [m.group(0)]

	print xmlFiles
			
		
	
getFiles()














