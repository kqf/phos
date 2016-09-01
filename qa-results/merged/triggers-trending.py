#!/usr/bin/python

import ROOT
import sys

def explore(data):
	for run in data: 
		print 'run ', run
		for sm in data[run]:
			print sm,
			for tru in data[run][sm]:
				print tru,
			print

def draw_multiple(hists, colors):
	map(lambda h, c: h.SetLineColor(c), hists, colors)
	map(lambda h: h.Draw("hist same"), hists)

	legend = ROOT.TLegend(0.88, 0.6, 0.93, 0.93)
	map(lambda h: legend.AddEntry(h, h.label), hists)
	return legend

def nicelydraw(tru):
	canvas = ROOT.TCanvas('test', 'test', 800, 707)
	ROOT.gStyle.SetOptFit(True)
	tru.Draw("colz")
		# fitf.Draw('same')
	canvas.SetGridy()
	# canvas.SetLogy()
	canvas.Update()
	raw_input('...')		

class TrendDrawer(object):
	def __init__(self, fname, quantity):
		super(TrendDrawer, self).__init__()
		self.ntrus = 8
		self.quantity = quantity
		self.colors = [8, 9, 38, 48, 41, 5, 12, 1]

		data = self.quantity.extract_modules(fname)
		self.draw_trending_plots(data)

	def form_trending_plots(self, sm, runs):
		namef = lambda x, y: 'h_%s_TRU_%s' % (str(x), str(y))
		nbins, title = len(runs), self.quantity.title
		hists = [ROOT.TH1F( namef(sm, i + 1), title % sm, nbins, 0, nbins) for i in range(self.ntrus)]
		for i, h in enumerate(hists): h.label = 'TRU ' + str(i + 1)

		for ibin, run in enumerate(sorted(runs)):
			for itru, tru in enumerate(runs[run]):
				val, err = runs[run][tru]
				hists[itru].SetBinContent(ibin + 1, val)
				hists[itru].SetBinError(ibin + 1, err)
				hists[itru].GetXaxis().SetBinLabel(ibin + 1, run)
		return hists

	def draw_trending_plots(self, data):
		for sm in sorted(data):
			hists  = [h for h in self.form_trending_plots(sm, data[sm]) if h.GetMaximum() > 0]
			hists[0].SetAxisRange(0.01, 1.01 * max(h.GetMaximum() for h in hists), 'Y');
			colors = self.colors[:len(hists)]
			canvas = ROOT.TCanvas('c' + str(sm), 'canvas', 1200, 403)
			legend = draw_multiple(hists, colors)
			legend.Draw('same')
			canvas.Update()
			raw_input('Press <ENTER> ...')

class Quantity(object):
	def __init__(self, title):
		super(Quantity, self).__init__()
		self.title = title
		self.threshod = 4.5
		self.maxenergy = 20.

	def extract_tru(self, tru):
		fitf = ROOT.TF1('fitf', "[0]", self.threshod, self.maxenergy)
		fitf.SetParameter(0, 0)
		tru.Fit(fitf, 'wrq')
		# tru.SetAxisRange(-0.01, 2.,"Y");
		# nicelydraw(tru)

		# i = tru.GetName()[-1]
		# return float(i), 0.

		return fitf.GetParameter(0), 0 #fitf.GetParError(0)

	def extract_run(self, run):
		return {tru.GetName(): self.extract_tru(tru) for tru in run }

	def extract_modules(self, fname):
		ifile = ROOT.TFile(fname)
		run_numbers = sorted(set([r.GetName().split('M')[0] for r in ifile.GetListOfKeys()]))
		supermods = [ 'M%d'%i for i in range(1, 5)]

		get_ratio = lambda x: [h for h in x if 'Ratio' in h.GetName()]
		raw  = {sm: {nrun: get_ratio(ifile.Get(nrun + sm)) for nrun in run_numbers} for sm in supermods}
		data = {sm: {nrun: self.extract_run(raw[sm][nrun]) for nrun in raw[sm]} for sm in raw}
		return data

def tru_coordinates(itru):
	assert (itru >= 1) and (itru <= 8), "Illegal TRU!!!\nCheck your code. TRU numeration starts is 1 .. 8" 
	n = itru - 1
	ncols, nrows, nmods = 7, 13, 4
	col, row = n % nmods, n / nmods
	x, y = 1 + col * (ncols + 1), 1 + row * (nrows + 1)
	return range(x, x + ncols), range(y, y + nrows)

			
class QuantityChannels(Quantity):
	def __init__(self, title):
		super(QuantityChannels, self).__init__(title)

	def extract_tru(self, itru, hist): 
		x, y = tru_coordinates(itru)
		# [hist.SetBinContent(i, j, 1)  for j in y for i in x]
		# value = sum(1  for j in y for i in x if hist.GetBinContent(i, j) > 0)
		value = hist.Integral(x[0], x[-1], y[0], y[-1])
		return value, 0

	def extract_run(self, perrun):
		res = {str(itru): self.extract_tru(itru, perrun) for itru in range(1, 9) }
		# print res
		# nicelydraw(perrun)
		return res

	def extract_modules(self, fname):
		ilist = ROOT.TFile(fname).L0
		run_numbers = sorted(r.GetName() for r in ilist)
		supermods = list('SM' + str(i) for i in range(1, 5))
		get_hist = lambda run, sm: ilist.FindObject(run).FindObject('h4x4Clu' + sm)
		raw  = {sm: {run: get_hist(run, sm) for run in run_numbers} for sm in supermods}

		get_nevents = lambda run : ilist.FindObject(run).FindObject('hNev').GetBinContent(1)
		for sm in raw: 
			for run in raw[sm]:
				raw[sm][run].Rebin2D(2, 2)
				raw[sm][run].Scale(1./ get_nevents(run))

		data = {sm: {run: self.extract_run(raw[sm][run]) for run in sorted(raw[sm])} for sm in raw}
		return data


		
def main():
	path = './' if len(sys.argv) < 2 else sys.argv[1]

	# ratio = Quantity("Trigered clusters / all clusters in %s in E > 4.5 GeV region;;Trigered clusters / all clusters")
	# TrendDrawer(path + 'ratio.root', ratio)

	channels = QuantityChannels("Number of TRU channels fired in %s;; # of TRU channels")
	TrendDrawer(path + 'TriggerQASingle.root', channels)


if __name__ == '__main__':
	main()