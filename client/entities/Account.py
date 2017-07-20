# -*- encoding:utf-8 -*-

from client import entity

class Account(entity.Entity):
	def __init__(self):
		super().__init__()
		print('client account created!!!')

	def become_player(self):
		print('client become player!')

		if self.server.login('dennis', 'dennis11'):
			print('login ok!')
		else:
			print('login not ok!')
