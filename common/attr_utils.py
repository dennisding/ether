# -*- coding:utf-8 -*-

from . import attr

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
	def __init__(self, baseType = None, options = '', default = None):
		self.baseType = baseType
		self.options = Options(options)
		self.default = default

		self.index = None
		self.global_attrs = {} # {index:attr}
		self.self_attrs = {} # {index:attr}

	def build_attributes(self, index, parent_info):
		self.index = index
		index = index + 1

		return index

	def set_index(self, index):
		self.index = index

	def set_parent(self, parent):
		self.global_attrs = parent.global_attrs

	def check(self, value):
		return True

	def new_instance(self, parent):
		pass

	def setup_value(self, parent, value):
		return value

class AttributeMetaclass(type):
	def __new__(cls, name, bases, namespace, **kwds):
		Type = type.__new__(cls, name, bases, namespace, **kwds)

		build_attributes(0, Type)

		return Type

def build_attributes(index, Type, parent = None, attr_info = None):
	# attr_info = AttrInfo(Type)
	attr_info = attr_info or AttrInfo(Type)

	attr_info.set_index(index)
	index = index + 1

	parent and attr_info.set_parent(parent)

	attrs = {} # {}
	for name, vlaue in inspect.getmembers(Type):
		if isinstance(value, attr.attr):
			attrs[name] = value
			index = setup_attributes(index, attrs, attr_info)

	Type._attr_info = attr_info

def setup_attributes(index, attrs, parent_attr_info):
	names = list(attrs.keys())
	names.sort()

	for name in names:
		attr = attrs[name]

		index = attr.build_attributes(index, parent_attr_info)

	return index
