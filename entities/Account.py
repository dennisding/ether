# -*- coding:utf-8 -*-

from game import entity

class Account(entity.Entity):
	_components = (
		'components.Login.Login',
	)
	def __init__(self):
		print('account init!!!', self.eid)

#		self.login_method()
#		self.login_method2()

	def login_method(self):
		print('account login method')