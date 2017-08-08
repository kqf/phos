#!/usr/bin/python


# TODO: Spilt this object across different configurables
# example 
#        options.spectrum.nsigmas = 5
# 		 options.spectrum.config = 'config/spectrum.json'
# 		 options.mass_range = (0.02, 0.06)

class Options(object):
	"""
		This is class should handle all possible variable! options 
		that i need to compare in my analysis.
	"""
	def __init__(self, relaxedcb = False, particle='pi0', average = {}, ptconfig='config/pt-analysis.json', priority = 999):
		super(Options, self).__init__()
		self.relaxedcb  = relaxedcb
		self.particle = particle
		self.average  = average
		self.ispi0 = 'pi0' in self.particle
		self.priority = priority
		self.pt_config = ptconfig
		self.spectrum_config = 'config/spectrum.json'
		self.invmass_config = 'config/invariant-mass.json'
		self.fit_mass_width = True
		self.nsigmas = 2