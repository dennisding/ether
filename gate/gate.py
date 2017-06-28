# -*- coding:utf-8 -*-

import asyncio
import engine

from . import client_service

class Gate:
	def __init__(self):
		engine._server = self

	def serve(self):
		self.start_client_service()
		self.start_game_service()

		self.run_forever()

	def start_client_service(self):
		self.client_service = client_service.ClientService()

		self.client_service.serve()

	def start_game_service(self):
		pass

	def run_forever(self):
		loop = asyncio.get_event_loop()
		loop.run_forever()