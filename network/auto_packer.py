# -*- encoding:utf-8 -*-

import struct
from . import packer

# basic types
TYPE_INT = 1
TYPE_U_INT = 2
TYPE_CHAR_INT = 3
TYPE_U_CHAR_INT = 4
TYPE_SHORT_INT = 5
TYPE_U_SHORT_INT = 6
TYPE_BOOL = 7
TYPE_FLOAT = 8
TYPE_STR = 9

# complex types
TYPE_LIST = 10
TYPE_SET = 11
TYPE_MAP = 12

#CUSTOM_PACKER
CUSTOM_PACKER_BEGIN = 64

TYPE_FORMAT = 'B'
TYPE_SIZE = struct.calcsize(TYPE_FORMAT)

_id_to_packers = {} # {packer_id:real_packer}
_type_to_packers = {} # {type:auto_packer}

class AutoPacker:
	def __init__(self, type_id, packer):
		self.type_id = type_id

		self.packer = packer

	def pack_into(self, buff_list, value):
		buff_list.append(struct.pack(TYPE_FORMAT, self.type_id))
		self.packer.pack_into(buff_list, value)

	def unpack(self, data, offset):
		type_id = struct.unpack_from(TYPE_FORMAT, data, offset)[0]
		offset = offset + TYPE_SIZE

		unpacker = _id_to_packers[type_id]
		offset, result = unpacker.unpack(data, offset)
		return offset, result

class AutoList:
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def pack_into(self, buff_list, values):
		# pack the size
		buff_list.append(struct.pack(self.size_format, len(values)))

		# pack the list item
		for value in values:
			packer = _type_to_packers[type(value)]
			packer.pack_into(buff_list, value)

	def unpack(self, data, offset):
		size = struct.unpack_from(self.size_format, data, offset)[0]
		offset = offset + self.size_size

		result = []
		for index in range(size):
			type_id = struct.unpack_from(TYPE_FORMAT, data, offset)[0]
			offset = offset + TYPE_SIZE

			unpacker = _id_to_packers[type_id]
			offset, item = unpacker.unpack(data, offset)
			result.append(item)

		return offset, result

class AutoSet:
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def pack_into(self, buff_list, values):
		buff_list.append(struct.pack(self.size_format, len(values)))

		for value in values:
			packer = _type_to_packers[type(value)]
			packer.pack_into(buff_list, value)

	def unpack(self, data, offset):
		size = struct.unpack_from(self.size_format, data, offset)[0]
		offset = offset + size

		result = set()
		for index in range(size):
			type_id = struct.unpack_from(TYPE_FORMAT, data, offset)[0]
			offset = offset + TYPE_SIZE

			unpacker = _id_to_packers[type_id]
			offset, item = unpacker.unpack(data, offset)
			result.add(item)

		return offset, item

class AutoMap:
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def pack_into(self, buff_list, values):
		buff_list.append(struct.pack(self.size_format, len(values)))

		for key, value in values.items():
			# pack key
			packer = _type_to_packers[type(key)]
			packer.pack_into(buff_list, key)
			# pack value
			packer = _type_to_packers[type(value)]
			packer.pack_into(buff_list, value)

	def unpack(self, data, offset):
		size = struct.unpack_from(self.size_format, data, offset)[0]
		offset = offset + self.size_size

		result = {}
		for index in range(size):
			type_id = struct.unpack_from(TYPE_FORMAT, data, offset)[0]
			offset = offset + TYPE_SIZE
			packer = _id_to_packers[type_id]
			offset, key = packer.unpack(data, offset)

			type_id = struct.unpack_from(TYPE_FORMAT, data, offset)[0]
			offset = offset + TYPE_SIZE
			packer = _id_to_packers[type_id]

			offset, value = packer.unpack(data, offset)
			result[key] = value

		return offset, result

def register(type_id, packer_name, types = (), real_packer = None):
	type_packer = real_packer or getattr(packer, packer_name)
	if isinstance(type_packer, type):
		type_packer = type_packer()

	_id_to_packers[type_id] = type_packer

	auto_packer = AutoPacker(type_id, type_packer)

	# setup types to packer
	if not isinstance(types, (list, tuple)):
		types = types,
	for pack_type in types:
		_type_to_packers[pack_type] = auto_packer

	if real_packer:
		name = packer_name
	else:
		name = 'Auto%s'%(packer_name)

	if hasattr(packer, name):
		raise RuntimeError('can"t not register packer (%s) twice'%(name))

	setattr(packer, name, auto_packer)

register(TYPE_INT, 'Int', int)
register(TYPE_U_INT, 'UInt') # no unsigend int in python
register(TYPE_CHAR_INT, 'CharInt') # no char int in python
register(TYPE_U_CHAR_INT, 'UCharInt')
register(TYPE_SHORT_INT, 'ShortInt')
register(TYPE_U_SHORT_INT, 'UShortInt')
register(TYPE_BOOL, 'Bool', bool)
register(TYPE_FLOAT, 'Float', float) # double is not supported
register(TYPE_STR, 'Str', str)
register(TYPE_LIST, 'AutoList', (list, tuple), AutoList)
register(TYPE_SET, 'AutoSet', set, AutoSet)
register(TYPE_MAP, 'AutoMap', dict, AutoMap)

def compile(type_list):
	return packer.compile(type_list)

if __name__ == '__main__':
	pk = compile('AutoMap, Bool, Int')
	data = pk.pack({1:True, 2:'aa', 'bb': {'a':'b'}}, True, 1024)
	result = pk.unpack(data)

	import zlib
	obj = zlib.compressobj()

	d1 = obj.compress(data)
	d11 = obj.flush(zlib.Z_SYNC_FLUSH)
	d2 = obj.compress(data)
	d3 = obj.flush(zlib.Z_SYNC_FLUSH)

	print('result!!!!!!', len(d1), len(d11), len(d2), len(d3), len(data), result)

	de = zlib.decompressobj()
	o1 = de.decompress(d1)
	o11 = de.decompress(d11)
	o2 = de.decompress(d2)
	o3 = de.decompress(d3)

	out = o1 + o11 + o2 + o3

	print('len:', len(out))
