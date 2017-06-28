# -*- encoding:utf-8 -*-

from . import auto_packer

class protocol:
	def __init__(self, *defines):
		self.parse_definitions(defines)

	def parse_definitions(self, defines):
		self.pdef = []
		arg_types = []

		for define in defines:
			if isinstance(define, pdef):
				self.pdef.append(define)
				arg_types.append(define.value_type)

		self.arg_types = ','.join(arg_types)

class pdef:
	def __init__(self, value_type, name):
		self.value_type = value_type
		self.name = name

class pret:
	pass
