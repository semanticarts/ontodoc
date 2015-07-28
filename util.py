""" Utility functions
"""

from yaml import load as load_yaml

def load_config():
	with open('config.yaml', 'rb') as conf:
		return load_yaml(conf)

def uri_to_qname(uri):
    parts = uri.split('#')
    if parts[0] == load_config()['namespace']:
    	return "%s%s%s" % (load_config()['prefix'], load_config()['separator'], parts[1])
    else:
    	return uri

def uri_to_anchor(uri):
	parts = uri.split('#')
	if parts[0] == load_config()['namespace']:
		return "#"+parts[1]
	else:
		return uri