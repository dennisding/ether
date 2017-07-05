# -*- coding:utf-8 -*-

class swallow:
	def __init__(self):
		pass

	def __getattr__(self, name):
		return self

	def __setattr__(self, name, value):
		return value

	def __call__(self, *kwds, **kdws):
		return self

	def __bool__(self):
		return False

