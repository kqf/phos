from comparator import Comparator
from ptplotter import PtPlotter
import ROOT

class LogItem(object):
	def __init__(self, name, histograms, multirange=False):
		super(LogItem, self).__init__()
		self.name = name
		self.histograms = histograms
		self.multirange = multirange
		


class AnalysisOutput(object):
	def __init__(self, label, particle):
		super(AnalysisOutput, self).__init__()
		self.particle = particle
		self.label = label
		self.pool = []

	def update(self, stepname, histograms, multirange=False):
		self.pool.append(
			LogItem(stepname, histograms, multirange)
		)

	def plot(self, stop=False):
		for item in self.pool:
			print 'Drawing', item.name
			if item.multirange:
				PtPlotter(
					item.histograms, 
					self.label, 
					self.particle
				).draw(stop, "{0}/{1}".format(self.label, item.name))
				continue

		for hist in item.histograms:
				diff = Comparator(
					stop=stop, 
					oname="{0}/{1}/{2}-{3}".format(self.label, item.name, hist.GetName(), self.particle)
				)
				diff.compare(hist)

	def append(self, other):
		self.pool.append(other.pool)