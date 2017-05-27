#!/usr/bin/python

import ROOT

# TODO: Add tests
# TODO: Make sure that all histograms have these properties

class TH(object):
	def __init__(self):
		pass

	@staticmethod
	def copy_properties(self, hist1, hist2):
	    if 'label'    in dir(hist1): hist1.label = hist2.label
	    if 'logy'     in dir(hist1): hist1.logy = hist2.logy
	    if 'priority' in dir(hist1): hist1.priority = hist2.priority
	    if 'fitfunc'  in dir(hist1): hist1.fitfunc = hist2.fitfunc
	    return hist1


