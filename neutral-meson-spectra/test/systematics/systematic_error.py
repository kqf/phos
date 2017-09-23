from spectrum.broot import BROOT as br

class SysError(object):
	def __init__(self, *args, **kwargs):
		super(SysError, self).__init__()
		self.prop = br.prop(*args, **kwargs)


	def histogram(self, hist, values = []):
		systhist = br.copy(hist)
		# Force saved options
		br.setp(systhist, self.prop)

		if not values:
			return systhist

		for bin, value in zip(br.range(hist), values):
			systhist.SetBinContent(bin, value)
		return systhist


		