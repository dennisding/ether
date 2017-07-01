# -*- coding:utf-8 -*-

import sys
import inspect

def extract_gadgets(namespace, funcs, items):
	for name, attr in items:
		if name.startswith('__') and name.endswith('__') and name != '__init__':
			continue

		if not inspect.isfunction(attr):
			assert name not in namespace
			namespace[name] = attr
			continue

		methods = funcs.setdefault(name, [])
		methods.append(attr)

def gather_component_gadgets(namespace, funcs, components):
	for component in components:
		# load the component methods
		tokens = component.split('.')
		module_name = '.'.join(tokens[:-1])
		component_name = tokens[-1]

		__import__(module_name)
		module = sys.modules[module_name]
		component = getattr(module, component_name)

		extract_gadgets(namespace, funcs, inspect.getmembers(component))

def gen_sequence_function(funcs):
	def _wrapper(*args, **kwds):
		for f in funcs:
			f(*args, **kwds)

	return _wrapper

def assemble_function(namespace, funcs):
	for name, fun in funcs.items():
		if len(fun) == 1:
			namespace[name] = fun[0]
			continue

		namespace[name] = gen_sequence_function(fun)

def assemble_components(namespace):
	components = namespace.get('_components')
	if not components:
		return namespace

	funcs = {}
	result = {}
	extract_gadgets(result, funcs, namespace.items())
	result.update(namespace)

	gather_component_gadgets(result, funcs, components)

	assemble_function(result, funcs)

	return result
