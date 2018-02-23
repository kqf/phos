
class AnalysisOutput(object):
	def __init__(self, label):
		super(AnalysisOutput, self).__init__()
		self.label = label
		self.mass = None
		self.ratio = None
		self.background = None
		self.signal = None
		self.ptwidth = None
		self.ptmass = None
		self.pool = []

	def update(self, hists):
		self.pool.append(hists)

	def plot(self):
		pass
