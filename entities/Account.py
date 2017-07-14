# -*- coding:utf-8 -*-

from game import entity

class Account(entity.LocalEntity):
	_components = (
		'components.Login.Login',
	)

	def __init__(self):
		print('account init!!!', self.eid)

