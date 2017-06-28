# -*- encoding:utf-8 -*-
# to do:
# 1. connection_made and connection_lost
# 2. check the client and server protocols
# 3. services design

import re
import asyncio

from . import filters

# server options, udp, zip, raw

class Remote:
	def __init__(self, master):
		self.master = master

	def __getattr__(self, name):
		def _fun(*args, **kwds):
			self.master.call_remote_method(name, *args, **kwds)

		return _fun

class Connection:
	def __init__(self, delegate, cid, master, options, send_service, receive_service):
		self.delegate = delegate
		self.cid = cid
		self.master = master
		self.options = options
		self.transport = None
		self.send_service = send_service
		self.receive_service = receive_service

		self.remote = Remote(self)

		self.setup_connection(options)

	def setup_connection(self, options):
		self.send_filter, self.receive_filter = filters.gen_filters(options)

	def connection_ready(self):
		self.delegate.connection_ready()

	# low level connection
	def connection_made(self, transport):
		self.transport = transport
		self.delegate.connection_made()
		self.master.connection_made(self)

	def connection_lost(self, exc):
		self.master.connection_lost(self, exc)
		self.delegate.connection_lost()

		# break the cycle reference
		self.__dict__.clear()

	def call_remote_method(self, name, *args, **kwds):
		data = self.send_service.pack(name, *args, **kwds)

		data = self.send_filter.filter(data)
		self.transport.write(data)

	def data_received(self, data):
		# to do : add the log when data is invalid
		for pack in self.receive_filter.feed(data):
			name, args = self.receive_service.unpack(pack)

			method = getattr(self.delegate, name, None)
			if method:
				method(*args)
			else:
				getattr(self, name)(*args)

	def eof_received(self):
		pass

class Server:
	def __init__(self, delegate_factory, options, send_service, receive_service):
		self.delegate_factory = delegate_factory

		self.parse_options(options)

		self.send_service = send_service
		self.receive_service = receive_service
		#self.services = services

		self.setup_server()

	def setup_server(self):
		self.connections = {} # {cid:connection}
		self.last_cid = 0
		self.port = 0

	def gen_cid(self):
		self.last_cid = self.last_cid + 1
		return self.last_cid

	def parse_options(self, options):
		self.options = set()

		for token in re.split('[ ,]', options):
			token = token.strip()
			if token:
				self.options.add(token)

	def connection_made(self, connection):
		# to do: check the signature
		connection.connection_ready()

	def connection_lost(self, connection, exc):
		self.connections.pop(connection.cid, None)

	def create_connection(self):
		cid = self.gen_cid()

		delegate = self.delegate_factory()

		connection = Connection(delegate, cid, self, self.options, \
									self.send_service, self.receive_service)
		delegate.connection = connection
		delegate.remote = connection.remote

		self.connections[connection.cid] = connection

		return connection

	def start(self, port, ip = ''):
		self.port = port

		# start server
		loop = asyncio.get_event_loop()
		routine = loop.create_server(self.create_connection, ip, self.port)
		loop.run_until_complete(routine)
		# loop.call_soon(routine)

if __name__ == '__main__':
	import service

	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	class Delegate:
		# connection set by server
		# remote set by server
		def connection_made(self):
			print('connection made')

		def connection_ready(self):
			print('connection ready')

		def connection_lost(self):
			print('connection lost')

		def login(self, name, password):
			self.remote.login(name == password)

	# services
	s = service.Service()
	s.build_protocols()

	def delegate_factory():
		return Delegate()

	server = Server(delegate_factory, 'zip pack, big', s)

	server.start(999)

	print('server start!!!!')

	loop = asyncio.get_event_loop()
	loop.run_forever()
