# -*- encoding:utf-8 -*-

from client import entity

class Avatar(entity.Entity):
	_components = ()

	def __init__(self):
		super().__init__()
		print('avatar created!!')

	def become_player(self):
		print('avtar become player')
