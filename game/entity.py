# -*- coding:utf-8 -*-

from . import entity_utils

from utils import assemble
from utils import swallow

class EntityMeta(type):
	def __new__(cls, name, bases, namespace, **kwds):
		namespace = assemble.assemble_components(namespace)

		return type.__new__(cls, name, bases, namespace)

class LocalEntity(metaclass = EntityMeta):
	gateid = None
	cid = None

	all_client = swallow.swallow()
	own_client = swallow.swallow()
	other_client = swallow.swallow()

	def __init__(self):
		pass

	def set_client(self, gateid, cid):
		print('set client!', gateid, cid)

		self.gateid = gateid
		self.cid = cid

		# create the client entity
		if self.gateid and self.cid:
			entity_utils.create_client_entity(self)

class Entity(LocalEntity):
	def __init__(self):
		pass
