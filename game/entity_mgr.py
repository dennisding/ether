# -*- coding:utf-8 -*-

import inspect
import pathlib

from . import entity

class EntityMgr:
	def __init__(self):
		self.types = {} # { name : Type}
		self.entities = {} # {eid:entity}

		self.last_eid = 0

	def gen_eid(self):
		self.last_eid = self.last_eid + 1
		return self.last_eid

	def load_entities(self, path):
		path = pathlib.Path(path)
		for name in path.iterdir():
			if not name.is_file():
				continue

			# don't import files
			if name.name.startswith('_') or name.suffix != '.py':
				continue

			module = __import__(name.stem)
			for name, attr in inspect.getmembers(module, inspect.isclass):
				if issubclass(attr, entity.Entity):
					assert name not in self.types
					self.types[name] = attr

	def get_entity(self, eid):
		return self.entities.get(eid)

	def del_entity(self, eid):
		entity = self.entities.pop(eid)

		entity.on_destroy()

	def create_entity(self, name, attrs = {}, eid = None):
		eid = eid or self.gen_eid()

		Type = self.types[name]

		entity = Type.__new__(Type)
		entity.__dict__.update(attrs)
		entity.eid = eid

		entity.__init__()

		self.entities[eid] = entity
		return eid