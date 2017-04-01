#!/usr/bin/python


class Options(object):
	"""
		This is class should handle all possible variable! options 
		that i need to compare in my analysis.
	"""
	def __init__(self, relaxedcb = False, particle='pi0', average = {}, ptconfig='config/pt-analysis.json'):
		super(Options, self).__init__()
		self.relaxedcb  = relaxedcb
		self.particle = particle
		self.average  = average
		self.ispi0 = 'pi0' in self.particle
		self.ptconfig = ptconfig