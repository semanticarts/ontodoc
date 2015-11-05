""" Process DTPs
"""

class OwlDatatypePropertyParser():

	def __init__(self, g):

		self.g = g
		self.datatypeProperties = {}

	def parse(self):

		datatypePropQuery = """
		SELECT ?prop ?superProp ?domain ?range ?type ?comment
		WHERE {
		  ?prop a owl:DatatypeProperty  
		  OPTIONAL {
		    ?prop rdfs:subPropertyOf ?superProp
		    FILTER (!isBlank(?superProp))
		  }
		  OPTIONAL {
		    ?prop rdfs:domain ?domain 
		    FILTER (!isBlank(?domain))
		  }
		  OPTIONAL { 
		    ?prop rdfs:range ?range 
		  	FILTER (!isBlank(?range))
		  }
		  OPTIONAL {
		    ?prop rdf:type ?type2 .
		    FILTER (?type not in (owl:DatatypeProperty))
		    FILTER (!isBlank(?type))
		  }
		  OPTIONAL { 
		  	?prop rdfs:comment ?comment 
			FILTER (!isBlank(?comment))
		  }
		}
		"""
		bindings = ['superProp', 'domain', 'range', 'type', 'comment']
		res = self.g.query(datatypePropQuery)
		for row in res:
			if row[0] not in self.datatypeProperties:
				self.datatypeProperties[str(row[0])] = {}
				for i,v in enumerate(row[1:]):
					if v != None:
						self.datatypeProperties[str(row[0])][bindings[i]] = [str(v)]
			else:
				for i,v in enumerate(row[1:]):
					if v != None:
						self.datatypeProperties[str(row[0])][bindings[i]].append(str(v))

		return self.datatypeProperties