# -*- encoding:utf-8 -*-

from client import entity

class Account(entity.Entity):
	def __init__(self):
		super().__init__()
		print('client account created!!!')

	def become_player(self):
		self.server.login(1, 1)
#		print('client become player!')
#
#		if self.server.login('dennis1', 'dennis1'):
#			print('login ok!')
#		else:
#			print('login failed!!!!!!')

	@rpc.rpc('Int, Int')
	def test(self, int1, int2):
		print('server to client test', int1, int2)
