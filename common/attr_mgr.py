# -*- coding:utf-8 -*-

class AttrMgr:
	def __init__(self):
#		self.values = values or {} # {index:values}
		self.values = {}


		self.parent = None
		self.changed = set()
		self.child_changed = set()

	def get_value(self, attr_info):
		if attr_info.index in self.values:
			return True, self.values[attr_info.index]

		return False, None

	def set_value(self, parent, attr_info, value):
		value = attr_info.setup_value(parent, value)

		self.values[attr_info.index] = value

		self.parent and self.parent.on_value_changed(attr_info)

	def on_value_changed(self, attr_info):
		if attr_info.index in self.changed:
			return

		self.changed.add(attr_info.index)

		self.parent and self.parent.on_child_changed(attr_info.parent)

	def on_child_changed(self, attr_info):
		if attr_info.index in self.child_changed:
			return

		self.child_changed.add(attr_info.index)

		self.parent and self.parent.on_child_changed(attr_info.parent)

	def new_instance(self, parent, attr_info):
		instance = attr_info.new_instance(parent)

		self.values[attr_info.index] = instance
		return instance
