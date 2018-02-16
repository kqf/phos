
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

	def plot(self):
		pass
