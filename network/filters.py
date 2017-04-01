# -*- encoding:utf-8 -*-

import zlib
import struct

class ZipFilter:
	def __init__(self):
		self.zipper = zlib.compressobj()
		self.unzipper = zlib.decompressobj()

	def filter(self, data):
		return self.zipper.compress(data) + self.zipper.flush(zlib.Z_SYNC_FLUSH)

	def feed(self, data):
		return [self.unzipper.decompress(data)]

class PackFilter:
	def __init__(self, big_chunk = False):
		if big_chunk:
			self.size_format = 'i'
		else:
			self.size_format = 'h'

		# for unfilter
		self.size_size = struct.calcsize(self.size_format)
		self.data = b''

	def filter(self, data):
		return struct.pack(self.size_format, len(data)) + data

	def feed(self, data):
		self.data = self.data + data

		result = []
		while True:
			if len(self.data) < self.size_size:
				break

			size = struct.unpack_from(self.size_format, self.data)[0]
			if len(self.data) < self.size_size + size:
				break

			package = self.data[self.size_size:self.size_size + size]
			result.append(package)
			self.data = self.data[self.size_size + size:]

		return result

class Filter:
	def __init__(self, filters):
		self.filters = filters

	def filter(self, data):
		for f in self.filters:
			data = f.filter(data)
		return data

	def feed(self, data):
		datas = data,

		for f in self.filters:
			result = []
			for d in datas:
				pack = f.feed(d)
				result.extend(pack)
			datas = result

		return result

def gen_filters(options):
	filters = []
	unpack_filter = []

	if 'pack' in options:
		big_chunk = 'big' in options
		filters.append(PackFilter(big_chunk))
	if 'zip' in options:
		filters.append(ZipFilter())

	reverse_filters = list(filters)
	reverse_filters.reverse()

	return Filter(filters), Filter(reverse_filters)

if __name__ == '__main__':
	pack, unpack = gen_filters(['zip', 'pack', 'big'])

	d1 = pack.filter(b'1')
	d2 = pack.filter(b'\00122')
	d3 = pack.filter(b'333')

	for data in unpack.feed(d1):
		print(data)
	for data in unpack.feed(d2 + d3):
		print(data)
