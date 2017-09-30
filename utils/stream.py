# -*- coding:utf-8 -*-

import struct

# write stream
class StructStream:
	def __init__(self):
		self.buff = []

	def get_data(self):
		return b''.join(self.buff)

	def write_char(self, value):
		self.buff.append(struct.pack('c', value))

	def write_short(self, value):
		self.buff.append(struct.pack('h', value))

	def write_int(self, value):
		self.buff.append(struct.pack('i', value))

	def write_float(self, value):
		self.buff.append(struct.pack('f', value))

	def write_str(self, value):
		self.buff.append(struct.pack('h', len(value)))
		self.buff.append(value.encode())

	def write_byte(self, value):
		self.buff.append(struct.pack('h', len(value)))
		self.buff.append(value)

# read stream
class ByteStream:
	def __init__(self, data):
		self.data = data
		self.offset = 0

	def read_char(self):
		data = struct.unpack_from('c', self.data, self.offset)
		self.offset = self.offset + 1
		return data[0]

	def read_short(self):
		data = struct.unpack_from('h', self.data, self.offset)
		self.offset = self.offset + 2
		return data[0]

	def read_int(self):
		data = struct.unpack_from('i', self.data, self.offset)
		self.offset = self.offset + 4
		return data[0]

	def read_float(self):
		data = struct.unpack_from('f', self.data, self.offset)
		self.offset = self.offset + 4
		return data[0]

	def read_str(self):
		size = struct.unpack_from('h', self.data, self.offset)
		self.offset = self.offset + 2 # size's size

		data = self.data[self.offset:self.offset + size]
		self.offset = self.offset + size
		return data.decode()

	def read_byte(self):
		size = struct.unpack_from('h', self.data, self.offset)
		self.offset = self.offset + 2 # size' size

		data = self.data[self.offset:self.offset + size]
		self.offset = self.offset + size

		return data