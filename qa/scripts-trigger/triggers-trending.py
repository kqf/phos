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
	styles  = [2, 3, 1, 1] * 2
	widths  = [2, 2, 1, 1] * 2
	markers = [34, 20, 21, 22] * 2
	map(lambda h, c: h.SetMarkerColor(c), hists, colors)
	map(lambda h, c: h.SetLineColor(c), hists, colors)
	map(lambda h: h.Draw("ep same"), hists)
	# for i, h in enumerate(hists): h.SetLineStyle(styles[i])
	# for i, h in enumerate(hists): h.SetLineWidth(widths[i])
	for i, h in enumerate(hists): h.SetMarkerStyle(markers[i])
	for i, h in enumerate(hists): h.SetMarkerSize(1.2)

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
	def __init__(self, path, fname, quantity):
		super(TrendDrawer, self).__init__()
		self.path = path
		self.ntrus = 8
		self.quantity = quantity
		self.colors = [8, 28, 38, 46, 41, 5, 12, 1]

		data = self.quantity.extract_modules(path + fname)
		self.draw_trending_plots(data)

	def form_trending_plots(self, sm, runs):
		namef = lambda x, y: 'h_%s_TRU_%s' % (str(x), str(y))
		nbins, title = len(runs), self.quantity.title
		hists = [ROOT.TH1F( namef(sm, i + 1), title % sm, nbins, 0, nbins) for i in range(self.ntrus)]
		for i, h in enumerate(hists): h.label = 'TRU ' + str(i + 1) # custom legend label

		for ibin, run in enumerate(sorted(runs)):
			for itru, tru in enumerate(runs[run]):
				val, err = runs[run][tru]
				hists[itru].SetBinContent(ibin + 1, val)
				hists[itru].SetBinError(ibin + 1, err)
				hists[itru].GetXaxis().SetBinLabel(ibin + 1, run)
				if ibin == 0: hists[itru].LabelsOption('v') # This is completely different thing: makes vertical bins

		return hists

	def draw_trending_plots(self, data):
		optstat = ROOT.gStyle.GetOptStat()
		ROOT.gStyle.SetOptStat(0)
		for sm in sorted(data):
			hists  = [h for h in self.form_trending_plots(sm, data[sm]) if h.GetMaximum() > 0]
			if not hists: 
				print 'No data available for', sm
				continue

			hists[0].SetAxisRange(0.01, 1.01 * max(h.GetMaximum() for h in hists), 'Y');
			colors = self.colors[:len(hists)]
			canvas = ROOT.TCanvas('c' + str(sm), 'canvas', 1200, 403)
			legend = draw_multiple(hists, colors)
			legend.Draw('same')
			canvas.SetGridx()
			canvas.SetGridy()
			canvas.Update()
			canvas.SaveAs(self.path + '/images/' + self.quantity.oname + '_' + sm + '.pdf')
			# raw_input('Press <ENTER> ...')
		ROOT.gStyle.SetOptStat(optstat)

class Quantity(object):
	def __init__(self, title):
		super(Quantity, self).__init__()
		self.title = title
		self.threshod = 4.5
		self.maxenergy = 20.
		self.oname = title.split()[0]

	def extract_tru(self, tru):
		fitf = ROOT.TF1('fitf', "[0]", self.threshod, self.maxenergy)
		fitf.SetParameter(0, 0)
		tru.Fit(fitf, 'wwrq')
		# tru.SetAxisRange(-0.01, 2.,"Y");
		# nicelydraw(tru)

		# i = tru.GetName()[-1]
		# return float(i), 0.

		return fitf.GetParameter(0), fitf.GetParError(0)

	def extract_run(self, run):
		return {tru.GetName(): self.extract_tru(tru) for tru in run }

	def extract_modules(self, fname):
		ifile = ROOT.TFile(fname)
		run_numbers = sorted(set([r.GetName().split('M')[0] for r in ifile.GetListOfKeys()]))
		run_numbers = [r for r in run_numbers if r.isdigit()]
		run_numbers = [r for r in run_numbers if int(r) > 257606]
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
	def __init__(self, title, **kwargs):
		super(QuantityChannels, self).__init__(title)
		self.cell_function = kwargs['cellf']
		self.histname = 'h4x4' + kwargs['cluster']
		self.nevents  = 'hNev'
		self.oname = title.split()[0] + kwargs['cluster']
		self.normalization = 1.

	def extract_tru(self, itru, hist): 
		x, y = tru_coordinates(itru)
		if not hist: return 137, 137
		# [hist.SetBinContent(i, j, 1)  for j in y for i in x]
		value, error = self.cell_function(hist, x, y, self.normalization)
		return value, error

	def extract_run(self, perrun):
		res = {str(itru): self.extract_tru(itru, perrun) for itru in range(1, 9) }
		# print res
		# nicelydraw(perrun)
		return res

	def extract_modules(self, fname):
		ilist = ROOT.TFile(fname).L0
		run_numbers = sorted(r.GetName() for r in ilist)
		run_numbers = [r for r in run_numbers if r.isdigit()]
		run_numbers = [r for r in run_numbers if int(r) > 257606]

		supermods = list('SM' + str(i) for i in range(1, 5))
		get_hist = lambda run, sm: ilist.FindObject(run).FindObject(self.histname + sm)
		raw  = {sm: {run: get_hist(run, sm) for run in run_numbers} for sm in supermods}

		get_nevents = lambda run : ilist.FindObject(run).FindObject(self.nevents).GetBinContent(1)
		for sm in raw: 
			for run in raw[sm]:
				if not raw[sm][run]:
					print 'ERROR: no data for ', run, sm
					continue
				raw[sm][run].Rebin2D(2, 2)
				# raw[sm][run].Scale(1./ get_nevents(run))
				self.normalization = get_nevents(run)

		data = {sm: {run: self.extract_run(raw[sm][run]) for run in sorted(raw[sm])} for sm in raw}
		return data

from math import sqrt
def integral(h, x, y, norm):
	val_err = ROOT.Double(0)
	val, norm_err = h.IntegralAndError(x[0], x[-1], y[0], y[-1], val_err), sqrt(norm)
	res, res_err = val / norm, sqrt( (val_err / norm) ** 2 + (norm_err * val / norm / norm) ** 2)
	print res, res_err
	return res, res_err

def nchannels(h, x, y, norm):
	val = sum(1  for j in y for i in x if h.GetBinContent(i, j) > 0)
	return val, sqrt(val)

		
def main():
	path = './' if len(sys.argv) < 2 else sys.argv[1]

	ratio = Quantity("Triggered clusters / all clusters in %s in E > 4.5 GeV region;;Triggered clusters / all clusters")
	TrendDrawer(path, 'ratio.root', ratio)

	trigfile = 'TriggerQASingle.root'
	draw_quantity = lambda q: TrendDrawer(path, trigfile, q)

	cluster_types = {'': '', 'matching cluters with E > 2 GeV': 'Clu'}
	for tp in cluster_types:
		cltype = cluster_types[tp]

		ctitle   = "Probability for TRUs in %s to be fired, " + tp + " ;; N_{Fired channels} / N_{kINT7}" 
		probability = QuantityChannels(ctitle, cluster=cltype, cellf=integral)
		draw_quantity(probability)

		ptitle   = "Number of TRU channels fired in %s " + tp + ";; # of TRU channels"
		channels = QuantityChannels(ptitle, cluster=cltype, cellf=nchannels)
		draw_quantity(channels)


if __name__ == '__main__':
	main()