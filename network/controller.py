# -*- encoding:utf-8 -*-

from .. import engine

def create_udp_server(protocol, address):
	event_loop = engine.event_loop()

	connect = event_loop.create_datagram_endpoint(protocol, address)
	event_loop.run_until_complete(connect)

def create_udp_services(protocol, addr):
	event_loop = engine.event_loop()

	future = event_loop.create_datagram_endpoint(protocol, \
		remote_addr = addr, reuse_address = True)

	event_loop.run_until_complete(future)

def create_udp_sender(protocol, addr):
	event_loop = engine.event_loop()

	future = event_loop.create_datagram_endpoint(protocol, \
		local_addr = addr, reuse_address = True, allow_broadcast = True)