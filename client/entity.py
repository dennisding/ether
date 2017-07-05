# -*- encoding:utf-8 -*-

from utils import assemble

class EntityMeta(type):
	def __new__(cls, name, bases, namespace, **kwds):
		namespace = assemble.assemble_components(namespace)

		return type.__new__(cls, name, bases, namespace)

class Entity(metaclass = EntityMeta):
	pass