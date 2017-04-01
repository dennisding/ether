# -*- encoding:utf-8 -*-

import asyncio

from network import server

class TestServer(server.Server):
	pass

if __name__ == '__main__':
	s = TestServer(99, 'zip')

	s.start()