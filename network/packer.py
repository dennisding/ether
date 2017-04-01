# -*- encoding:utf-8 -*-

import struct

def format_packer(packer):
	if isinstance(packer, type):
		return packer()

	return packer

class TypeBase:
	format = ''
	size = 0

	def pack_into(self, buff_list, value):
		buff_list.append(struct.pack(self.format, value))

	def unpack(self, data, offset = 0):
		result = struct.unpack_from(self.format, data, offset)[0]
		return self.size + offset, result

class CharInt(TypeBase):
	format = 'b'
	size = struct.calcsize(format)

class UCharInt(TypeBase):
	format = 'B'
	size = struct.calcsize(format)

class ShortInt(TypeBase):
	format = 'h'
	size = struct.calcsize(format)

class UShortInt(TypeBase):
	format = 'H'
	size = struct.calcsize(format)

class Int(TypeBase):
	format = 'i'
	size = struct.calcsize(format)

class UInt(TypeBase):
	format = 'I'
	size = struct.calcsize(format)

class Bool(TypeBase):
	format = '?'
	size = struct.calcsize(format)

class Float(TypeBase):
	format = 'f'
	size = struct.calcsize(format)

class Str:
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def pack_into(self, buff_list, value):
		format = '%s%ds'%(self.size_format, len(value))
		buff_list.append(struct.pack(format, len(value), value.encode()))

	def unpack(self, data, offset = 0):
		size = struct.unpack_from(self.size_format, data, offset)[0]
		offset = offset + self.size_size
		result = struct.unpack_from('%ss'%(size), data, offset)

		return offset + size, result[0].decode()

class List:
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def __init__(self, inner_type):
		self.inner_type = format_packer(inner_type)

	def pack_into(self, buff_list, values):
		buff_list.append(struct.pack(self.size_format, len(values)))

		for value in values:
			self.inner_type.pack_into(buff_list, value)

	def unpack(self, data, offset):
		size = struct.unpack_from(self.size_format, data, offset)[0]
		offset = offset + self.size_size

		result = []
		for index in range(size):
			offset, item = self.inner_type.unpack(data, offset)
			result.append(item)

		return offset, result

class Set:
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def __init__(self, inner_type):
		self.inner_type = format_packer(inner_type)

	def pack_into(self, buff_list, values):
		buff_list.append(struct.pack(self.size_format, len(values)))

		for value in values:
			self.inner_type.pack_into(buff_list, value)

	def unpack(self, data, offset):
		size = struct.unpack_from(self.size_format, data, offset)[0]
		offset = offset + self.size_size

		result = set()
		for index in range(size):
			offset, item = self.inner_type.unpack(data, offset)
			result.add(item)

		return offset, result

class Map:
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def __init__(self, key_type, value_type):
		self.key_type = format_packer(key_type)
		self.value_type = format_packer(value_type)

	def pack_into(self, buff_list, value):
		buff_list.append(struct.pack(self.size_format, len(value)))

		for key, value in value.items():
			self.key_type.pack_into(buff_list, key)
			self.value_type.pack_into(buff_list, value)

	def unpack(self, data, offset):
		size = struct.unpack_from(self.size_format, data, offset)[0]
		offset = offset + self.size_size

		result = {}
		for index in range(size):
			offset, key = self.key_type.unpack(data, offset)
			offset, value = self.value_type.unpack(data, offset)
			result[key] = value
		return offset, result

class packer:
	def __init__(self, *packers):
		self.packers = self.format_packers(packers)

	def format_packers(self, packers):
		result = []
		for packer in packers:
			result.append(format_packer(packer))

		return result

	def pack(self, *values):
		result = []
		for value, packer in zip(values, self.packers):
			packer.pack_into(result, value)
		return b''.join(result)

	def unpack(self, data, offset = 0):
		result = []
		for packer in self.packers:
			offset, item = packer.unpack(data, offset)
			result.append(item)

		return result

def compile(format):
	code = 'packer(%s)'%(format)
	return eval(code)

if __name__ == '__main__':
	pk = compile('Int, Str, List(Float), Set(Str), Map(Int, Str), Int')

	data = pk.pack(1, 'haha', [1,2,3], set(['aa', 'bb', 'cc']), \
			{1: 'haha', 2: 'bb'}, 1024)
	result = pk.unpack(data)

	print('result!!!', len(data), result)
