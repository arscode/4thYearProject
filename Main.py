

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

		for attribute in Openflow:
			path = '/request/openflow/'+attribute
			element = tree.xpath(path)
			if element:
				self.openflow[attribute] = (element[0].text).strip()
		self.application = tree.xpath("application")[0].text


class RequestStore:
	requests = []

	def __init__(self,xmlFiles):
		for xmlFile in xmlFiles:
			request = Request(xmlFile)
			self.requests += [request]
				
	def printRequests(self):
		for r in self.requests:
			print r.application
			print  r.openflow.values()
	



#put in requeststore?
def getFiles():
	allFiles = os.listdir(os.getcwd())
	xmlFiles = []
	xmlPattern= re.compile('^.*\.(xml)$')
	for fileName in allFiles:
		m = re.match(xmlPattern,fileName)
		if m and fileName != "FlowSchema.xml":
			xmlFiles += [m.group(0)]
	print xmlFiles
	return xmlFiles


			
		
	
allRequests = RequestStore(getFiles())
allRequests.printRequests()












