# -*- encoding:utf-8 -*-

import asyncio
import controller

class Channel:
	pass

class UdpServer:
	def __init__(self, port, services):
		pass

class Remote:
	def __init__(self, master):
		self.master = master

	def __getattr__(self, name):
		def _caller(*args, **kwds):
			self.master.call_remote_method(name, *args, **kwds)

		return _caller

class UdpClient(asyncio.Protocol):
	def __init__(self, port, services):
		self.port = port
		self.remote_addr = ('0.0.0.0', port)
		self.services = services

		self.transport = None

		self.remote = Remote(self)

		controller.create_udp_sender(lambda : self, self.remote_port)

	def connection_made(self, transport):
		self.transport = transport

	def call_remote_method(self, name, *args, **kwds):
		data = self.services.pack(name, *args, **kwds)

		self.transport.sendto(data)

class UdpService(asyncio.Protocol):
	def __init__(self, port, services):
		self.port = port
		self.services = services

	def datagram_received(self, data, addr):
		name, args = self.services.unpack(data)

		getattr(self, name)(*args)

	def start(self):
		controller.create_udp_services(lambda : self, ('127.0.0.1', self.port))

if __name__ == '__main__':
	from protocol import protocol, pdef, pret, Services

	class GameMgrService(Services):
		gate_started = protocol( pret('Bool'),
			pdef('Str', 'ip'),
			pdef('Str', 'port')
		)

	server = UdpServer(999, GameMgrSercies())

	msg = GameMgrServices.gate_started.instance('127.0.0.1', 886)
	ok = yield from server.call_rpc(msg)

	server.gate_started(ip = '255.255.255.255', port = 998)
