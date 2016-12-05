#!/usr/bin/python

import json
import sys
import ROOT 
ROOT.TH1.AddDirectory(False)

def update():
	canvas = ROOT.gROOT.FindObject('c1')
	canvas.Update()
	canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
	ROOT.gApplication.Run(True)

def draw_hist(hist):
	hist.Draw()
	update


class YieldEstimator(object):
	def __init__(self, filenme, energy = '7TeV', prates = '', yrange = (-0.12, 0.12), checky = False):
		super(YieldEstimator, self).__init__()
		self.energy = energy.replace('T', ' T')
		with open(prates, 'r') as f:
			self.prates = json.load(f)
		self.checky = checky
		self.raw_hist = self.extract_data(filenme) 
		self.default = self.calculate(*yrange) 

	def normalization(self, hist):
		func = ROOT.TF1('tsallis', '[3] *' + self.prates['Tsallis'], 0.5, 25.)
		for i, p in enumerate(self.prates['Parameters Tsallis ' + self.energy]): 
			func.FixParameter(i, p)
		func.SetParameter(3, 1)
		hist.Fit(func, 'R')
		update()
		return func.GetParameter(3)

	def extract_data(self, filenme):
		infile = ROOT.TFile(filenme)
		raw, counter = infile.fhEtaMC, infile.hCounter
		norm = self.normalization(infile.hgenPi0)
		raw.Scale(1. / counter.GetBinContent(1)/ norm)
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
		pt.SetTitle(self.energy + ' MC pythia; p_{t}, GeV/c; #frac{1}{N_{ev}}#frac{d^{2}N}{dp_{t}dy}')
		pt.label = 'mc'
		pt.energy = self.energy
		return pt

	def draw(self):
		draw_hist(self.default)

	def adjusted_bins(self, n = 16):
		self.default.Rebin(n)
		self.default.Scale(1./ n)
		return self.default 

def check_multiple(gyield):
	for i in [4, 8, 10, 14, 16]:
		print i

		hist = gyield.calculate(-1. * i / 100., i/ 100.)
		hist.SetLineColor(i)
		hist.Draw('same')
	update()

class CocktailYield(YieldEstimator):
	def __init__(self, filenme, energy = '7TeV', prates = '', yrange = (-0.12, 0.12), checky = False):
		super(CocktailYield, self).__init__(filenme, energy, prates, yrange, checky)

	def extract_data(self, filenme):
		infile = ROOT.TFile(filenme)
		raw, counter = [infile.fhGammaMCPi0, infile.fhGammaMCEta, infile.fhGammaMCOmega], infile.hCounter
		rates = self.prates[self.energy]
		norm = self.normalization(infile.hgenPi0)
		map(lambda x, y: x.Scale(y / norm), raw, rates)
		for h in raw[1:]: raw[0].Add(h)
		raw = raw[0]
		# raw.Scale(1. / counter.GetBinContent(1))
		return raw	
		

def double_ratio(decay_photons, direct_photons, label):
	ratio = decay_photons.Clone('double_ratio' + label.replace(' ', ''))
	ratio.SetTitle('Double Ratio MC, ' + decay_photons.energy + '; p_{t}, GeV/c; R_{d} #approx #frac{#gamma inclul}{#gamma decay}')
	ratio.Add(direct_photons)
	ratio.Divide(decay_photons)
	ratio.label = label

	for i in range(direct_photons.GetNbinsX()):
		if not (direct_photons.GetBinContent(i + 1) > 0):
			ratio.SetBinContent(i + 1, 0)
			ratio.SetBinError(i + 1, 0)
	return ratio


def draw_multiple(histograms, log=True):
	# find the biggest hist and draw it 
	colors = [37, 46, 8]

	# Delete label if exists
	histograms[0].SetTitle(histograms[0].GetTitle().split('|')[0])
	histograms[0].Draw('hist')

	for h, c in zip(histograms[1:], colors): h.SetLineColor(c)
	for h, c in zip(histograms[1:], colors): h.SetMarkerColor(c)
	# for h in histograms[1:]: h.SetMarkerStyle(20)
	for h in histograms[1:]: h.Draw('same')

	legend = ROOT.TLegend(0.9, 0.4, 1.0, 0.6)
	for h in histograms: legend.AddEntry(h, h.label)

	legend.Draw('same')
	ROOT.gPad.SetLogy(log)
	update()

def get_arguments():
	parameters = sys.argv[1:]
	if len(parameters) < 5: 
		return parameters + ['']
	return parameters


def main():
	decay_sim, direct_photons_dir, energy, prates, cocktail = get_arguments()

	estimator = CocktailYield(decay_sim, energy, prates) if cocktail else YieldEstimator(decay_sim, energy, prates)
	decay_photons = estimator.adjusted_bins()

	pQCD = direct_photons_dir + '%s.root'
	direct_photons = [ROOT.TFile(pQCD % i).hnnl for i in ['0.5', '1', '2']]
	for d in direct_photons: d.label = d.GetTitle().split('|')[1]

	draw_multiple([decay_photons] + direct_photons)


	ratios = [double_ratio(decay_photons, d, d.label) for d in direct_photons]
	draw_multiple(ratios, False)
	check_multiple(estimator)

if __name__ == '__main__':
	main()
