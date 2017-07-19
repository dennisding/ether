# -*- coding:utf-8 -*-

import inspect
import pathlib

from network import service

class TypeInfos:
	def __init__(self, name, Type, client_service, server_service):
		self.name = name
		self.Type = Type
		self.client_service = client_service
		self.server_service = server_service

class EntityMgr:
	def __init__(self):
		self.type_infos = {} # { name : TypeInfos}
		self.entities = {} # {eid:entity}
		self.defs = {} # {name:defs}
		self.protocol_path = ''

		self.last_eid = 0

	def gen_eid(self):
		self.last_eid = self.last_eid + 1
		return self.last_eid

	def set_protocol_path(self, path):
		self.protocol_path = path

	def prepare_entities(self, def_path, entity_path, BaseType):
		self.iter_py_files(def_path, self.gen_def)

		def _gen_type(name):
			self.gen_type(name, BaseType)
		self.iter_py_files(entity_path, _gen_type)

	def gen_def(self, name):
		module = {}
		content = open(name).read()
		exec(content, module)

		Client = module.get('Client')
		Server = module.get('Server')

		if Client == None and Server == None:
			return

		def _gen_service(Type):
			if Type:
				return service.gen_service(Type())
			return service.gen_service()

		client_service = _gen_service(Client)
		server_service = _gen_service(Server)

		self.defs[name.stem] = client_service, server_service

	def iter_py_files(self, path, callback):
		path = pathlib.Path(path)
		for name in path.iterdir():
			if not name.is_file():
				continue

			if name.name == '__init__.py' or name.suffix != '.py':
				continue

			callback(name)

	def gen_type(self, name, BaseType):
		module = __import__(name.stem)
		for name, attr in inspect.getmembers(module, inspect.isclass):
			if issubclass(attr, BaseType):
				assert name not in self.type_infos
				self.setup_type_infos(name, attr)

	def setup_type_infos(self, name, attr):
		defs = self.defs.get(name)

		self.type_infos[name] = TypeInfos(name, attr, defs[0], defs[1])

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
