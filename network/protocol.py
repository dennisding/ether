# -*- encoding:utf-8 -*-

class protocol:
	def __init__(self, *defines):
		self.pret = None

		self.parse_definitions(defines)

	def parse_definitions(self, defines):
		self.pdef = []
		arg_types = []

		for define in defines:
			if isinstance(define, pdef):
				self.pdef.append(define)
				arg_types.append(define.value_type)
			elif isinstance(define, pret):
				assert self.pret == None
				self.pret = define

		self.arg_types = ','.join(arg_types)

class pdef:
	def __init__(self, value_type, name):
		self.value_type = value_type
		self.name = name

class pret:
	def __init__(self, value_type, name):
		self.value_type = value_type
		self.name = name

class attr:
	def __init__(self, value_type, options):
		self.value_type = value_type
		self.options = options
