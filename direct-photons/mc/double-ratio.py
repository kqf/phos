#!/usr/bin/python

import ROOT 
ROOT.TH1.AddDirectory(False)

def update():
	ROOT.gROOT.FindObject('c1').Update()
	raw_input('Press ENTER ...')

def draw_hist(hist):
	hist.Draw()
	update


class YieldEstimator(object):
	def __init__(self, filenme, yrange = (-0.12, 0.12), checky = False):
		super(YieldEstimator, self).__init__()
		self.checky = checky
		self.raw_hist = self.extract_data(filenme) 
		self.default = self.calculate(*yrange) 


	def extract_data(self, filenme):
		infile = ROOT.TFile(filenme)
		raw, counter = infile.fhEtaMC, infile.hCounter
		raw.Scale(1. / counter.GetBinContent(1))
		return raw


	def calculate(self, ya, yb):
		if self.checky:
			y = self.raw_hist.ProjectionY('y')
			y.SetAxisRange(ya, yb, 'x')
			draw_hist(y)

		bin = lambda x : self.raw_hist.GetYaxis().FindBin(x)
		a, b = bin(ya), bin(yb)
		pt = self.raw_hist.ProjectionX('pythia_%d_%d' % (a, b), a, b)
		pt.Scale(1./(yb - ya))
		pt.SetTitle('MC pythia; p_{t}, GeV/c; #frac{1}{N_{ev}}#frac{d^{2}N}{dp_{t}dy}')
		return pt

	def draw(self):
		draw_hist(self.default)

def check_multiple(gyield):
	for i in [4, 8, 10, 14, 16]:
		print i

		hist = gyield.calculate(-1. * i / 100., i/ 100.)
		hist.SetLineColor(i)
		hist.Draw('same')
		update()



def main():
	pp_7tev = YieldEstimator('decay-photons/FastGen_pp/generated.root')
	decay_photons = pp_7tev.default
	direct_photons = ROOT.TFile('direct-photons/nnl.root').nnl
	decay_photons.Draw()
	direct_photons.Draw('same')
	ROOT.gPad.SetLogy()
	update()



	# check_multiple(pp_7tev)

if __name__ == '__main__':
	main()
