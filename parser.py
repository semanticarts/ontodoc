""" A wrapper for the parser functionality 
	(just exposes one method to aprse)
"""

import os
import rdflib


class Parser():

	def __init__(self, owl_directory='owl'):
		self.classes = {}
		self.objectProperties = {}
		self.datatypeProperties = {}
		self.instances = {}
		self.g = rdflib.Graph()
		for f in os.listdir(owl_directory):
			self.g.load('%s/%s' % (owl_directory, f))


	def parse(self):

		classQuery = """
		SELECT distinct ?s ?label
		WHERE { 
			?s a owl:Class .
			OPTIONAL { ?s rdfs:label ?label }
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


		instancesQuery = """
		SELECT distinct ?instance ?label ?comment
		WHERE {
		  ?instance rdf:type ?type .
		  OPTIONAL { ?instance rdfs:label ?label }
		  OPTIONAL { ?instance rdfs:comment ?comment }
		  FILTER (?type not in (owl:Class, owl:ObjectProperty, owl:DatatypeProperty, owl:AnnotationProperty, owl:Ontology))
		  FILTER ( !isBlank(?instance) )
		}
		"""

		res = self.g.query(instancesQuery)


		for inst, label, comment in res:
			if str(inst) not in self.instances:
				self.instances[str(inst)] = {
					'label': [l for l in [str(label),] if label != 'None'],
					'comment': [str(comment)]
				}

			else:
				self.instances[str(inst)]['label'].append(str(label))
				self.instances[str(inst)]['comment'].append(str(comment))

		return {
			'classes': self.classes,
			'objectProperties': self.objectProperties,
			'datatypeProperties': self.datatypeProperties,
			'instances': self.instances
		}

