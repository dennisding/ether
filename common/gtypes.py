# -*- coding:utf-8 -*-

import operator

from . import attr
from . import attr_mgr
from . import attr_utils

class RawType:
	baseType = None

	def __new__(cls, *args):
		return cls.baseType(*args)

	@classmethod
	def _setup_value(self, parent, value):
		pass

	@classmethod
	def check(cls, value):
		return isinstance(value, cls.baseType)

	def to_stream(self, attr, stream):
		pass

	def from_stream(self, attr, stream):
		pass

	def to_dict(self, filter = operator.truth):
		pass

	def from_dict(self, d):
		pass

class Int(RawType):
	baseType = int

class Float:
	pass

class Attribute:
	def __init__(self):
		self._attr_mgr = attr_mgr.AttrMgr()

	@classmethod
	def _setup_value(self, parent, value):
		pass

	@classmethod
	def check(cls, value):
		return True

	def to_stream(self, attr, stream):
		pass

	def from_stream(self, setter, stream):
		pass

	def to_dict(self, filter = operator.truth):
		return {}

	def from_dict(self, attrs):
		for index, attr in self._attr_info.self_attrs.items():
			if attr.name not in attrs:
				continue

			value = attr.new_instance(self)
			value = attr.base_type.from_dict(value, attrs[attr.name])

			self._attr_mgr.raw_set(index, value)

	@classmethod
	def _from_dict(self, d):
		print(self._attr_info)

def build_attributes(name, bases, namespaces):
	new_type = type(name, bases, namespaces)
	attribute = attr.attr(new_type)
	attribute.build_attributes()

	return new_type

class EntityAttribute(Attribute, metaclass = build_attributes):
	pass
