# -*- coding:utf-8 -*-

import re
import inspect

class Options:
	valie_options = set(('own_client', 'other_clients', 'all_clients', 'save', 'server'))
	def __init__(self, options):
		self.own_client = False
		self.other_clients = False
		self.server = True
		self.save = False

		for token in re.split('[\W,]', options):
			if not token:
				continue

			option = token
			value = True
			if token.startswith('no_'):
				option = token[3:]
				value = False

			setter = getattr(self, 'on_set_%s'%(option), None)
			if setter:
				setter(value)
			else:
				setattr(self, option, value)

	def on_set_all_clients(self, value):
		self.own_client = value
		self.other_clients = value

class AttrInfo:
	def __init__(self, base_type, options = '', default = None):
		self.base_type = base_type
		self.options = Options(options)
		self.default = default

#		base_type._attr_info = self
#		print('base type', base_type, self)

		self.name = None
		self.full_paths = []
		self.parent_paths = []
		self.global_attrs = {}
		self.self_attrs = {}
		self.parent = None

	def set_name(self, name):
		self.name = name

	def add_attribute(self, index, attr):
		self.global_attrs[index] = attr
		self.self_attrs[index] = attr

	def set_parent(self, parent):
		self.global_attrs = parent.global_attrs
		self.parent = parent

	def update_paths(self):
		if not self.parent:
			return

	def check(self, value):
		return True

	def new_instance(self, parent):
		# value = self.base_type(parent = parent)
		value = self.base_type()
		self.setup_value(parent, value)

		return value

	def setup_value(self, parent, value):
		self.base_type._setup_value(parent, value)

	def build_attributes(self, index, name, parent):
		self.index = index
		index = index + 1

		self.base_type._attr_info = self

		self.name = name

		parent and self.set_parent(parent)

		attrs = {}
		for name, value in inspect.getmembers(self.base_type):
			if isinstance(value, attr):
				attrs[name] = value

		return self.setup_attributes(index, attrs)

	def setup_attributes(self, index, attrs):
		names = list(attrs.keys())
		names.sort()

		for name in names:
			attr = attrs[name]

			index = attr.build_attributes(index, name, self)

			self.add_attribute(index, attr)

		return index

class attr:
	def __init__(self, base_type, options = '', default = None):
		self.attr_info = AttrInfo(base_type, options, default)

	def build_attributes(self, index = 0, name = '', parent_info = None):
		return self.attr_info.build_attributes(index, name, parent_info)

	def __get__(self, instance, owner):
		attr_mgr = instance._attr_mgr
		exist, value = attr_mgr.get_value(self.attr_info)
		if exist:
			return value

		return attr_mgr.new_instance(instance, self.attr_info)

	def __set__(self, instance, value):
		assert self.attr_info.check(value)

		instance._attr_mgr.set_value(instance, self.attr_info, value)
