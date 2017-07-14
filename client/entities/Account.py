# -*- encoding:utf-8 -*-

from client import entity

class Account(entity.Entity):
	def __init__(self):
		print('client account created!!!')

	def become_player(self):
		print('become player!')
