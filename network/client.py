# -*- encoding:utf-8 -*-

import re
import time
import asyncio

from . import filters

class Remote:
	def __init__(self, master):
		self.master = master

	def __getattr__(self, name):
		def _fun(*args, **kwds):
			return self.master.call_remote_method(name, *args, **kwds)

		return _fun

class Client(asyncio.Protocol):
	def __init__(self, delegate, options, send_service, receive_service):
		self.delegate = delegate
		self.send_service = send_service
		self.receive_service = receive_service

		self.parse_options(options)

		self.transport = None
		self.ip = ''
		self.port = 0

		self.setup_data_filter()

	def setup_data_filter(self):
		self.send_filter, self.receive_filter = filters.gen_filters(self.options)

	def call_remote_method(self, name, *args, **kwds):
		data = self.send_service.pack(name, *args, **kwds)

		data = self.send_filter.filter(data)

		self.transport.write(data)

	def parse_options(self, options):
		self.options = set()
		for token in re.split('[ ,]', options):
			token = token.strip()
			self.options.add(token)

	def connect(self, ip, port, callback = None, timeout = 0):
		self.ip = ip
		self.port = port

		loop = asyncio.get_event_loop()
		routine = loop.create_connection(lambda : self, self.ip, self.port)

		if not callback:
			loop.run_until_complete(routine)
			return

		# await time out
		begin_time = time.time()
		def done_callback(future):
			exception = future.exception()
			if timeout > 0 and (time.time() - begin_time > timeout):
				callback and callback(False)
				return

			# reconnect
			if exception: # re connected
				routine = loop.create_connection(lambda : self, self.ip, self.port)
				future = asyncio.ensure_future(routine)
				future.add_done_callback(done_callback)
			else:
				callback(True)

		future = asyncio.ensure_future(routine)
		future.add_done_callback(done_callback)

	def connection_made(self, transport):
		self.transport = transport

		self.delegate.remote = Remote(self)

		self.delegate.connection_made()
		# to do: check the signature
		self.delegate.connection_ready()

	def connection_lost(self, exc):
		self.delegate.connection_lost()

	def data_received(self, data):
		for package in self.receive_filter.feed(data):
			name, args = self.receive_service.unpack(package)

			getattr(self.delegate, name)(*args)

	def eof_received(self):
		pass

if __name__ == '__main__':
	import service

	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	s = service.Service()
	s.build_protocols()

	class Delegate:
		def connection_made(self):
			print('client connection made!')
			#self.remote.login('dennis', 'dennis')

		def connection_lost(self):
			print('client connection lost!!!')

		def connection_ready(self):
			print('client connection ready')

	c = Client(Delegate(), 'zip pack,big', s)

	def _connected(ok):
		print('client connected!!!!', ok)

	c.connect('127.0.0.1', 999, _connected)

	print('client started!!!')
	asyncio.get_event_loop().run_forever()

