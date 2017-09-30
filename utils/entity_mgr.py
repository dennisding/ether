# -*- coding:utf-8 -*-

import inspect
import pathlib

from . import entity_utils

from network import service
from common import attr_mgr

class TypeInfos:
	def __init__(self, name, Type, client_service, server_service, properties):
		self.name = name
		self.Type = Type
		self.client_service = client_service
		self.server_service = server_service
		self.properties = properties

		Type.type_info = self

		self.setup_properties()

	def setup_entity(self, entity, attrs):
		# update attributes
		entity.type_infos = self
		entity._attr_mgr = attr_mgr.AttrMgr()
		self.properties.from_dict(entity, attrs)

	def setup_properties(self):
		if not self.properties:
			entity_type._attr_info = attr.AttrInfo(self.Type)
			return

		entity_type = self.Type
		entity_type._attr_info = self.properties._attr_info

		for index, attr in self.properties._attr_info.self_attrs.items():
			assert not hasattr(entity_type, attr.name)

			setattr(entity_type, attr.name, attr)

class TypeDef:
	def __init__(self, name):
		self.name = name

		self.name_to_def = {}
		self.index_to_def = {}

		self.type_string = ''

	def get_def_by_name(self, name):
		return self.name_to_def[name]

	def get_def_by_index(self, index):
		return self.index_to_def[index]

	def build_defs(self, name, base_type):
		self.name = name

		tmp = [] # attribute, [0, type, name, options]

		for name, value, in inspect.getmembers(base_type):
			if isinstance(value, attr.attr):
				pass

	def build_type_string(self):
		tmp = ['@%s'%(self.name)]

		self.type_string = b' '.join(tmp)
		return self.type_string

	def add_attr(self, index, base_type, name):
		print('add_attr', index, base_type, name)
		attr = attr.attr(base_type)
		attr.set_index(index)
		attr.set_path(name)

		assert name not in self.name_to_def
		assert index not in self.index_to_def

		self.name_to_def[name] = attr
		self.index_to_def[index] = attr

	def add_rpc(self, index, ret, args, name):
		print('add_rpc', index, ret, args, name)

		rpc = rpc.rpc(args, ret)
		rpc.set_index(index)
		rpc.set_name(name)

		assert name not in self.name_to_def
		assert index not in eslf.index_to_def

		self.name_to_def[name] = rpc
		self.index_to_def[index] = rpc

class EntityMgr:
	def __init__(self):
		self.type_infos = {} # { name : TypeInfos}
		self.entities = {} # {eid:entity}
		self.defs = {} # {name:defs}

	def get_entity_defs(self):
		# format
		# @Avatar Int#hp Int#package.count Ret#Arg#rpc_name
		client_def = b'@Account 1#Int#hp 2#Package#package 3#Int#package.count 4###client_test'
		server_def = b'@Account 4###server_test'
		return client_def, server_def

	def set_entity_defs(self, client_defs, server_defs):
		type_def = None
		for token in client_defs.split():
			if token[0] == '@':
				type_def = TypeDef(token[1:])
				continue

			infos = token.split('#')
			if len(infos) == 3: # magic number 1#Int#package.count
				type_def.add_attr(*infos)
			elif len(infos) == 4: # magic number 4#Ret#Args#rpc_name
				type_def.add_rpc(*infos)

		self.defs[type_def.name] = type_def

	def gen_eid(self):
		return entity_utils.gen_eid()

	def prepare_entities(self, def_path, entity_path, BaseType):
		self.iter_py_files(def_path, self.gen_def)

		def _gen_type(name):
			try:
				self.gen_type(name, BaseType)
			except:
				print('[ERROR] gen type <%s> error!'%(name))
				raise
		self.iter_py_files(entity_path, _gen_type)

	def get_type_infos(self, name):
		return self.type_infos[name]

	def get_entity_type_list(self, fun):
		result = []
		for key, value in self.type_infos.items():
			if fun(value.Type):
				result.append(key)

		return result

	def gen_def(self, name):
		module = {}
		content = open(name).read()
		try:
			exec(content, module)
		except:
			print('[ERROR] generate def <%s> error!'%(name))
			raise

		Client = module.get('Client')
		Server = module.get('Server')
		Property = module.get('Property')

		if Client == None and Server == None:
			return

		def _gen_service(Type):
			if Type:
				return service.gen_service(Type())
			return service.gen_service()

		client_service = _gen_service(Client)
		server_service = _gen_service(Server)

		self.defs[name.stem] = client_service, server_service, Property

	def iter_py_files(self, path, callback):
		path = pathlib.Path(path)
		for name in path.iterdir():
			if not name.is_file():
				continue

			if name.name == '__init__.py' or name.suffix != '.py':
				continue

			callback(name)

	def get_type_list(self, BaseType):
		result = []
		for name, type_infos in self.type_infos.items():
			if issubclass(type_infos.Type, BaseType):
				result.append(name)

		return result

	def gen_type(self, name, BaseType):
		module = __import__(name.stem)
		for name, attr in inspect.getmembers(module, inspect.isclass):
			if issubclass(attr, BaseType):
				assert name not in self.type_infos
				self.setup_type_infos(name, attr)

	def setup_type_infos(self, name, entity_type):
		defs = self.defs.get(name)
		if not defs:
			defs = None, None, None

		self.type_infos[name] = TypeInfos(name, entity_type, defs[0], defs[1], defs[2])

	def get_entity(self, eid):
		return self.entities.get(eid)

	def del_entity(self, eid):
		entity = self.entities.pop(eid)

		entity.on_destroyed()

	def create_entity(self, name, attrs = {}, eid = None):
		eid = eid or self.gen_eid()

		type_infos = self.type_infos[name]
		Type = type_infos.Type

		entity = Type.__new__(Type)
		entity.eid = eid

		type_infos.setup_entity(entity, attrs)

		entity.__init__()

#		entity.clear_attrs_changed()

		self.entities[eid] = entity

		entity.on_created()

		return eid
