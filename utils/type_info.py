# -*- coding:utf-8 -*-

class TypeInfo:
	def __init__(self, name, namespace):
		self.name = name

		self.base_type = None

	def set_type(self, base_type):
		self.base_type = base_type

def gen_type_info(name, namespace):
	pass