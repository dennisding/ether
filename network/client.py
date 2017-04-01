# -*- encoding:utf-8 -*-

import re
import filters
import asyncio

class Remote:
	def __init__(self, master):
		self.master = master

	def __getattr__(self, name):
		def _fun(*args, **kwds):
			return self.master.call_remote_method(name, *args, **kwds)

		return _fun

class Client(asyncio.Protocol):
	def __init__(self, delegate, options, services):
		self.delegate = delegate
		self.services = services

		self.parse_options(options)

		self.transport = None
		self.ip = ''
		self.port = 0

		self.setup_data_filter()

	def setup_data_filter(self):
		self.send_filter, self.receive_filter = filters.gen_filters(self.options)

	def call_remote_method(self, name, *args, **kwds):
		data = self.services.pack(name, *args, **kwds)

		data = self.send_filter.filter(data)

		self.transport.send(data)

	def parse_options(self, options):
		self.options = set()
		for token in re.split('[ ,]', options):
			token = token.strip()
			self.options.add(token)

	def connect(self, ip, port):
		self.ip = ip
		self.port = port

		# run server
		loop = asyncio.get_event_loop()
		routine = loop.create_connection(lambda : self, self.ip, self.port)
		loop.run_until_complete(routine)
		# loop.call_soon(routine)

	def connection_made(self, transport):
		self.transport = transport

		self.delegate.remote = Remote(self)

		self.delegate.connection_made()

	def data_received(self, data):
		for package in self.receive_filter.feed(data):
			name, args = self.services.unpack(data)

			getattr(self.delegate, name)(*args)

if __name__ == '__main__':
	import service

	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	s = service.Service()
	s.build_protocols()

	class Delegate:
		def connection_made(self):
			pass
			#self.remote.login('dennis', 'dennis')

	c = Client(Delegate(), 'zip pack,big', s)

	c.connect('127.0.0.1', 999)

	asyncio.get_event_loop().run_forever()

