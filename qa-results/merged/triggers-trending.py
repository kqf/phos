#!/usr/bin/python

import ROOT
import sys

def get_tru_ratio(tru, threshod = 4.5, maxenergy = 20.):
	fitf = ROOT.TF1('fitf', "[0]", threshod, maxenergy)
	fitf.SetParameter(0, 0)
	tru.Fit(fitf, 'wrq')
	tru.SetAxisRange(-0.01, 2.,"Y");
	# canvas = ROOT.TCanvas('test', 'test', 800, 707)
	# ROOT.gStyle.SetOptFit(True)
	# tru.Draw("pl")
	# fitf.Draw('same')
	# canvas.SetGridy()
	# canvas.SetLogy()
	# canvas.Update()
	# raw_input('...')		
	return fitf.GetParameter(0), fitf.GetParError(0)

def extract_ratios(inlist):
	histograms = {int(h.GetName()[-1]) : h for h in inlist if 'Ratio' in h.GetName()}
	histograms = [histograms[k] for k in sorted(histograms)]
	res = [get_tru_ratio(tru) for tru in histograms]
	return res

def get_trending_hists(run_numbers, ntrus = 8):
	nbins = len(run_numbers)
	hists = [ROOT.TH1F("hTRU%d" % i, "hTRU%d" % i, nbins, 0, nbins) for i in range(1, ntrus + 1)]
	for k, h in enumerate(hists):
		[h.GetXaxis().SetBinLabel(i + 1, r) for i , r in enumerate(run_numbers)]
		h.label = h.GetName()
		h.SetAxisRange(0.01, 1.2,"Y");
		h.LabelsOption("v");
		h.SetLineWidth(3)
	[h.SetLineColor(c) for h, c in zip(hists, [8, 9, 38, 48, 41, 5, 12, 1][::-1]) ]

	return hists


def draw_trending_plots(data, run_numbers, ofile):
	hists = get_trending_hists(run_numbers)
	fout = ROOT.TFile(ofile, 'update')
	for sm, smdata in enumerate(zip(*data)):

		smname = "SM%d" % (sm + 1)
		for h in hists: 
			h.SetTitle("Trigered clusters / all clusters in " + smname + " in E > 4.5 GeV region")
			h.GetYaxis().SetTitle('Trigered clusters / all clusters')

		for i, k in enumerate(zip(*smdata)): 
			print k
			for j, (v, e) in enumerate(k):
				hists[i].SetBinContent(j + 1, v)
				hists[i].SetBinError(j + 1, e)

		canvas = ROOT.TCanvas(smname + '_trend', smname, 1000, 707)
		legend = ROOT.TLegend(0.88, 0.6, 0.93, 0.93)
		# canvas.SetLogy()
		canvas.SetGridx()
		canvas.SetGridy()
		map(lambda x: legend.AddEntry(x, x.label), hists)

		ROOT.gStyle.SetOptStat(0)
		for h in hists: h.Draw("same hist")
		legend.Draw('same')
		canvas.Show()
		canvas.Update()
		canvas.Write();
		fout.Write()
		raw_input('...')		
	fout.Close()



def main():
	path = './' if len(sys.argv) < 2  else sys.argv[1]
	print path
	ifile = ROOT.TFile(path + "ratio.root")
	run_numbers = sorted(set([r.GetName().split('M')[0] for r in ifile.GetListOfKeys()]))

	supermods = [ 'M%d'%i for i in range(1, 5)]
	data = [ [ifile.Get(nrun + sm) for sm in supermods] for nrun in run_numbers]
	data = [[ extract_ratios(sm) for sm in run] for run in data]

	draw_trending_plots(data, run_numbers, path + "/ResultsTriggerQA.root")



if __name__ == '__main__':
	main()