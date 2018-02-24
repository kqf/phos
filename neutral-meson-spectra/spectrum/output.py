class LogItem(object):
	def __init__(self, name, histograms, multirange=False):
		super(LogItem, self).__init__()
		self.name = name
		self.histograms = histograms
		self.multirange = multirange
		


class AnalysisOutput(object):
	def __init__(self, label):
		super(AnalysisOutput, self).__init__()
		self.label = label
		self.pool = []

	def update(self, stepname, histograms, multirange=False):
		self.pool.append(
			LogItem(stepname, histograms, multirange)
		)

	def plot(self):
		pass
