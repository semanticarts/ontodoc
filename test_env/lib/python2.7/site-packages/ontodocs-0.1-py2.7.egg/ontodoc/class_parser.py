""" Process classes
"""

class OwlClassParser():

	def __init__(self, g):

		self.g = g
		self.classes = {}

	def parse(self):

		classQuery = """
		SELECT distinct ?s ?label
		WHERE { 
			?s a owl:Class .
			OPTIONAL { ?s rdfs:label ?label }
			FILTER (!isBlank(?s))
		}
		"""

		res = self.g.query(classQuery)
		for uri, label in res:
			self.classes[str(uri)] = {
				'label': str(label)
			}

			self.classes[str(uri)]['comments'] = [str(c) for c, in self.g.query("""
			SELECT ?comment WHERE {
				<%s> rdfs:comment ?comment
			}""" % str(uri))]
		
			self.classes[str(uri)]['subclasses'] = [str(c) for c, in self.g.query("""
			SELECT ?SubClass WHERE { 
				{ <%s> rdfs:superClassOf ?SubClass . } 
				UNION 
				{ <%s> ^rdfs:subClassOf ?SubClass . }
			}""" % (str(uri), str(uri)))]

			self.classes[str(uri)]['superclasses'] = [str(c) for c, in self.g.query("""
			SELECT ?SuperClass WHERE { 
				{ <%s> rdfs:subClassOf ?SuperClass . } 
				UNION
				{ <%s> ^rdfs:superClassOf ?SuperClass . }
				FILTER (!isBlank(?SuperClass))
			}""" % (str(uri), str(uri)))]

			self.classes[str(uri)]['disjoints'] = [str(c) for c, in self.g.query("""
			SELECT ?disjoint WHERE { 
				<%s> owl:disjointWith ?disjoint 
			}""" % str(uri))]

			self.classes[str(uri)]['domain'] = [str(c) for c, in self.g.query("""
			SELECT ?domain { OPTIONAL {
				<%s> rdfs:domain ?domain . }
			}"""  % str(uri)) if str(c) != 'None']

			self.classes[str(uri)]['range'] = [str(c) for c, in self.g.query("""
			SELECT ?range { OPTIONAL {
				<%s> rdfs:range ?range . }
			}"""  % str(uri)) if str(c) != 'None']

		return self.classes