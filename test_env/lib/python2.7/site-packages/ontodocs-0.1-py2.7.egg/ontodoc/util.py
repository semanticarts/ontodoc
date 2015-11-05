""" Utility functions
"""

from yaml import load as load_yaml

def load_config():
	with open('config.yaml', 'rb') as conf:
		return load_yaml(conf)

def uri_to_qname(uri):
    if load_config()['namespace'] in uri:
    	return "%s:%s" % (load_config()['prefix'], uri.replace(load_config()['namespace'], ''))
    else:
    	return uri

def uri_to_anchor(uri):
	if load_config()['namespace'] in uri:
		return "#" + uri.replace(load_config()['namespace'], '')
	else:
		return uri