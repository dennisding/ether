# -*- coding:utf-8 -*-

from . import gtypes

from utils import stream

class Options:
	def __init__(self, options):
		self.options = options

class rpc:
	def __init__(self, arg_str, ret = '', options = ''):
		self.arg_str = arg_str

		self.parse_args()
		self.ret = ret
		self.options = Options(options)

	def parse_args(self):
		self.args = []

		env = gtypes.__dict__
		code = '(%s,)'%(self.arg_str)
		args = exec(code, env, env)

		for arg in args:
			if isinstance(arg, type):
				self.args.append(arg())
			else:
				self.args.append(arg)

	def pack_args(self, *args):
		stream = stream.StructStream()

		for index, arg in enumerate(args):
			packer = self.args[index]
			packer.to_stream(arg, stream)

		return stream.get_data()

	def unpack_args(self, stream):
		args = []
		for index, packer in enumerate(self.args):
			args.append(packer.from_stream(offset, stream))
		return args
