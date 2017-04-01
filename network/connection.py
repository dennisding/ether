# -*- encoding:utf-8 -*-

import struct

class Connection:
	def __init__(self, master):
		self.master = master
		self.transport = None

		self.last_exception = None

	def connection_made(self, transport):
		self.transport = transport

		self.master.connection_made(self)

	def connection_lost(self, exc):
		self.last_exception = exc

		self.master.connection_lost(self)

	def error_received(self, exc):
		self.last_exception = exc

		self.master.error_received(self)

class RawConnection(Connection):
	def data_received(self, data):
		self.master.data_received(data)

	def send_data(self, data):
		self.transport.write(data)

class UdpConnection(Connection):
	def datagram_received(self, data, addr):
		self.master.data_received(data)

	def send_data(self, data):
		self.transport.write(data)

class PackageConnection(Connection):
	size_format = 'h'
	size_size = struct.calcsize(size_format)

	def __init__(self, master):
		super().__init__(master)

		self.data = b''

	def send_data(self, data):
		self.transport.write(struct.pack(self.size_format, len(data)))
		self.transport.write(data)

	def data_received(self, data):
		self.data = self.data + data

		while True:
			if len(self.data) < self.size_size:
				break

			size = struct.unpack_from(self.size_format, self.data)
			if self.size_size + size < self.data:
				break

			package = self.data[self.size_size:self.size_size + size]
			self.data = self.data[self.size_size + size:]