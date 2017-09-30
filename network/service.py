# -*- encoding:utf-8 -*-

import asyncio
import hashlib

from .protocol import protocol, pdef, attr
from . import auto_packer

INDEX_TYPE = 'ShortInt'

check_signature = protocol(
	pdef('Str', 'local_sign'),
	pdef('Str', 'remote_sign')
)

class Protocol:
	def __init__(self, name, index, protocol):
		self.name = name
		self.index = index

		self.protocol = protocol
		self.packer = None
		self.return_packer = None

		self.set_index_type(INDEX_TYPE)

	def has_return(self):
		return bool(self.return_packer)

	def get_signature(self):
		return ':n:%s:a:%s'%(self.name, self.protocol.arg_types)

	def set_index_type(self, type_name):
		arg_types = '%s,%s'%(type_name, self.protocol.arg_types)
		self.packer = auto_packer.compile(arg_types)

		if self.protocol.pret:
			return_types = '%s, %s'%(type_name, self.protocol.pret.value_type)
			self.return_packer = auto_packer.compile(return_types)

	def pack(self, *args, **kwds):
		return self.packer.pack(self.index, *args)

	def unpack(self, data):
		return self.packer.unpack(data)[1:] # ignore the index

	def pack_return(self, value):
		return self.return_packer.pack(self.index, value)

	def unpack_return(self, data):
		return self.return_packer.unpack(data)[1]

class Service:
	def __init__(self, *services):
		self.services = list(services)

		self.reset()

		self.index_packer = auto_packer.compile(INDEX_TYPE)

	def reset(self):
		self.name_to_protocols = {}
		self.index_to_protocols = {}

		self.last_index = 0
		self.signature = b''

		self.services.sort(key = lambda a: type(a).__name__ )

	def gen_index(self):
		self.last_index = self.last_index + 1
		return self.last_index

	def build_protocols(self):
		self.reset()
		digest = hashlib.md5()

		self.add_base_protocols(digest)

		for service in self.services:
			self.add_service(service, digest)

		self.signature = digest.digest()

	def add_base_protocols(self, digest):
		self.add_protocol('_check_signature', check_signature, digest)

	def add_service(self, service, digest):
		service = type(service)

		digest.update(b':c:' + service.__name__.encode())

		names = dir(service)
		names.sort()

		for name in names:
			value = getattr(service, name)
			if isinstance(value, protocol):
				self.add_protocol(name, value, digest)
			elif isinstance(value, attr):
				self.add_attr(name, value, digest)

	def add_attr(self, name, value, digest):
		pass

	def add_protocol(self, name, protocol, digest):
		assert name not in self.name_to_protocols

		index = self.gen_index()

		p = Protocol(name, index, protocol)

		digest.update(b':p:' + p.get_signature().encode())

		self.name_to_protocols[name] = p
		self.index_to_protocols[index] = p

	def get_protocol_by_name(self, name):
		return self.name_to_protocols.get(name)

	def pack(self, name, *args, **kwds):
		protocol = self.name_to_protocols[name]

		return protocol.pack(*args, **kwds)

	def unpack(self, data):
		result = self.index_packer.unpack(data)
		index = self.index_packer.unpack(data)[0]
		protocol = self.index_to_protocols[index]

		return protocol.name, protocol.unpack(data)

	def pack_return(self, name, value):
		protocol = self.name_to_protocols[name]
		return protocol.pack_return(value)

	def unpack_return(self, data):
		result = self.index_packer.unpack(data)
		index = self.index_packer.unpack(data)[0]

		protocol = self.index_to_protocols[index]
		return protocol.unpack_return(data)

def gen_service(*services):
	s = Service(*services)
	s.build_protocols()

	return s
