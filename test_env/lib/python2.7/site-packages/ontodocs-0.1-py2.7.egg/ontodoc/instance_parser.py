""" Process Individuals
"""

class InstanceParser():

	def __init__(self, g):
		
		self.g = g
		self.instances = {}

	def parse(self):

		instancesQuery = """
		SELECT distinct ?instance ?label ?comment
		WHERE {
		  ?instance rdf:type ?type .
		  OPTIONAL { ?instance rdfs:label ?label }
		  OPTIONAL { ?instance rdfs:comment ?comment }
		  FILTER (?type not in (
		  		owl:Class, owl:ObjectProperty, 
		  		owl:DatatypeProperty, 
		  		owl:AnnotationProperty, 
		  		owl:Ontology,
		  		owl:FunctionalProperty,
		  		owl:TransitiveProperty,
		  		owl:SymmetricProperty,
		  		owl:InverseFunctionalProperty,
		  		rdfs:Property
		  	))
		  FILTER ( !isBlank(?instance) )
		}
		"""

		res = self.g.query(instancesQuery)


		for inst, label, comment in res:
			if str(inst) not in self.instances:
				self.instances[str(inst)] = {
					'label': [l for l in [str(label),] if str(label) != 'None'],
					'comment': [l for l in [str(comment),] if str(comment) != 'None']
				}

			else:
				if str(label) != 'None':
					self.instances[str(inst)]['label'].append(str(label))
				if str(comment) != 'None':
					self.instances[str(inst)]['comment'].append(str(comment))

		return self.instances