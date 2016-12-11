#!/usr/bin/python
# Convert cell X,Z to absID without geometry.
# Be careful in case if gemetry changes. 

import json
import sys

class Converter(object):
	sizex, sizez = 64, 56
	size = sizex * sizez 
	feex, feez = 16, 2
	cellmsg = '\nCell numbering ranges from: (0,0) to (63, 55)'
	feemsg = '\nFEE numbering ranges from: (0,0) to (3, 27)'

	def __init__(self, input_file):
		super(Converter, self).__init__()
		self.cells, self.fees = self.read(input_file)
		assert self.cells or self.fees, "Nothing to convert!"

	def read(self, input_file):
		with open(input_file, 'r') as f:
			data = json.load(f)
		return data['cells'], data['fees']

	def convert(self):
		cells, fees = [], []
		if self.cells: 
			cells = map(self.convert_cell, *zip(*self.cells))

		if self.fees:
			fees = map(self.convert_fee, *zip(*self.fees))
			
		all_cells = sum(fees, cells)

		print ','.join(map(str, all_cells))
		print len(all_cells), '      length of the sequence'


	def convert_cell(self, x, z, sm):
		# In this convention (0, 0, 1) is a first cell of module 1.
		assert x < self.sizex, "X cooridnate of cell is wrong x = %d !!!%s" % (x, self.cellmsg)
		assert z < self.sizez, "Z cooridnate of cell is wrong z = %d !!!%s" % (z, self.cellmsg)

		return (sm - 1) * self.size + x * self.sizez + z + 1

	def convert_fee(self, x, z, sm):
		assert x < self.sizex / self.feex, "X cooridnate of FEE is wrong x = %d !!!%s" % (x, self.feemsg)
		assert z < self.sizez / self.feez, "Z cooridnate of FEE is wrong z = %d !!!%s" % (z, self.feemsg)

		x, z = self.feex * x, self.feez * z
		# Convert fee coordinate to a set of 32 cell coordinates
		cells = [ (i, j, sm) for i in range(x, x + self.feex) for j in range(z, z + self.feez)]
		return map(self.convert_cell, *zip(*cells))

def main():
	if len(sys.argv) < 2: 
		print 'Usage: ./convert-xz-to-abs.py cells.json'
	Converter(sys.argv[1]).convert()

if __name__ == '__main__':
	main()