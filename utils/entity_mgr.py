# -*- coding:utf-8 -*-

import inspect
import pathlib

class TypeInfos:
	def __init__(self, name, Type):
		self.name = name
		self.Type = Type

class EntityMgr:
	def __init__(self):
		self.type_infos = {} # { name : TypeInfos}
		self.entities = {} # {eid:entity}
		self.protocol_path = ''

		self.last_eid = 0

	def gen_eid(self):
		self.last_eid = self.last_eid + 1
		return self.last_eid

	def set_protocol_path(self, path):
		self.protocol_path = path

	def load_entities(self, path, BaseType):
		path = pathlib.Path(path)
		for name in path.iterdir():
			if not name.is_file():
				continue

			if name.name == '__init__.py' or name.suffix != '.py':
				continue

			module = __import__(name.stem)
			for name, attr in inspect.getmembers(module, inspect.isclass):
				if issubclass(attr, BaseType):
					assert name not in self.type_infos
					self.setup_type_infos(name, attr)

	def setup_type_infos(self, name, attr):
		self.type_infos[name] = TypeInfos(name, attr)

	def get_entity(self, eid):
		return self.entities.get(eid)

	def del_entity(self, eid):
		entity = self.entities.pop(eid)

	def create_entity(self, name, attrs = {}, eid = None):
		eid = eid or self.gen_eid()

		type_infos = self.type_infos[name]
		Type = type_infos.Type

		entity = Type.__new__(Type)
		entity.__dict__.update(attrs)
		entity.eid = eid
		entity.type_infos = type_infos

		entity.__init__()

		self.entities[eid] = entity

		return eid
