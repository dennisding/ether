# -*- coding:utf-8 -*-

from . import assemble

class EntityMeta(type):
	def __new__(cls, name, bases, namespace, **kwds):
		namespace = assemble.assemble_components(namespace)

		return type.__new__(cls, name, bases, namespace)
