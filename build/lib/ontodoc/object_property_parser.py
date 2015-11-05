""" Process classes
"""

class OwlObjectPropertyParser():
	def __init__(self, g):
		self.g = g
		self.objectProperties = {}

	def parse(self):
		objectPropQuery = """
		SELECT ?prop ?type ?domain ?range ?inverse ?comment
		WHERE {
		    ?prop rdf:type owl:ObjectProperty .
		    OPTIONAL {
		      ?prop rdf:type ?type 
		      FILTER (?type not in (owl:ObjectProperty))
		      FILTER (!isBlank(?type))
		    }
		  	OPTIONAL {
		      ?prop rdfs:comment ?comment
		      FILTER (!isBlank(?comment))
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
		      ?prop owl:inverseOf ?inverse
		      FILTER (!isBlank(?inverse))
		    }
		}"""
		bindings = ['type', 'domain', 'range', 'inverse', 'comment']
		res = self.g.query(objectPropQuery)
		
		for row in res:
			if str(row[0]) not in self.objectProperties:
				self.objectProperties[str(row[0])] = {}
				for i,v in enumerate(row[1:]):
					if v != None:
						self.objectProperties[str(row[0])][bindings[i]] = [str(v)]
			else:
				for i,v in enumerate(row[1:]):
					if v != None:
						self.objectProperties[str(row[0])][bindings[i]].append(str(v))

		return self.objectProperties