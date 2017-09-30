# -*- coding:utf-8 -*-

from game import entity

class Avatar(entity.Entity):
	_components = (
	)

	def __init__(self):
		print('avatar init!!')

	def test(self):
		self.hp = 1024
		self.model_ids = [] # glist

		self.equips = [] # [EquipInfo]
		equip_info = self.equips[1]
		equip_info.gems = {}

		self.tasks = {} # {task_id:Task}, gmap

		task = self.tasks[task_id]

		task.finished = True

