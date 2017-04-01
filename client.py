# -*- encoding:utf-8 -*-

import asyncio

class Client(asyncio.Protocol):
	def connection_made(self, transport):
		self.transport = transport

		# self.transport.write('udp msg')
		self.transport.sendto(b'udp msg')

	def error_received(self, exc):
		print('error!!!!!', exc)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	server = loop.create_datagram_endpoint(Client, \
		remote_addr = ('255.255.255.255', 99), allow_broadcast = True, reuse_address = True)

	loop.run_until_complete(server)
	loop.run_forever()
