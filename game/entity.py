# -*- coding:utf-8 -*-

from utils import assemble

class EntityMeta(type):
	def __new__(cls, name, bases, namespace, **kwds):
		# to do: generate the component method
		namespace = assemble.assemble_components(namespace)

		return type.__new__(cls, name, bases, namespace)

class LocalEntity(metaclass = EntityMeta):
	def __init__(self):
		pass

	def on_entity_created(self):
		pass

	def on_entity_destroy(self):
		pass

	def _set_client(self, gid, cid):
		print('set client!', gid, cid)

class Entity(LocalEntity):
	def __init__(self):
		pass
