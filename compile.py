from jinja2 import Environment, FileSystemLoader
from parser import Parser
from util import load_config, uri_to_qname, uri_to_anchor
import datetime
#import sass

jinja_env = Environment(loader=FileSystemLoader('templates'), autoescape=False)
jinja_env.filters['to_link'] = uri_to_anchor
jinja_env.filters['to_qname'] = uri_to_qname
jinja_env.globals['timestamp'] = datetime.datetime.now().strftime('%A, %b %d %Y at %X')

def compile():
	
	owl_parser = Parser()
	page_data = { 
		'ontology': owl_parser.process(),
		'metadata': load_config()['site_info'] }

	#print data_dict
	
	with open('templates/base.html', 'rb') as base_template_file, \
		open('output/index.html', 'wB') as output:
		template = jinja_env.get_template( 'base.html')
		rendered_html = template.render(page_data=page_data)
		output.write(rendered_html)



if __name__ == '__main__':
	compile()