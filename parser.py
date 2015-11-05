""" A wrapper for the parser functionality 
	(just exposes one method to aprse)
"""

import os
import rdflib

from processing.class_parser import OwlClassParser
from processing.datatype_property_parser import OwlDatatypePropertyParser
from processing.object_property_parser import OwlObjectPropertyParser
from processing.instance_parser import InstanceParser


class Parser():

	def __init__(self, owl_directory='owl'):

		self.g = rdflib.Graph()
		for f in os.listdir(owl_directory):
			self.g.load('%s/%s' % (owl_directory, f))


	def process(self):

		return {
			'classes': OwlClassParser(self.g).parse(),
			'objectProperties': OwlObjectPropertyParser(self.g).parse(),
			'datatypeProperties': OwlDatatypePropertyParser(self.g).parse(),
			'instances': InstanceParser(self.g).parse()
		}

