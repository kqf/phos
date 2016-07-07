#!/usr/bin/env python2

from ROOT import TFile
import ROOT

def draw_and_save(name, draw=False, save=True):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs('pictures/' + name + '.pdf')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)

class BufferDrawer(object):
    def __init__(self, fill):
        self.histograms = []
        self.exclusion = ' '
        self.legends = []
        self.canvas = self.GetCanvas()
        self.fill = fill

    def GetCanvas(self):
        canvas = ROOT.gROOT.FindObject('c1')
        if not canvas: canvas = ROOT.TCanvas('c1', 'Resonances analysis', 1900, 400)
        return  canvas

    def Update(self, histo):
        self.histograms.append(histo)
        
    def FindNecessaryHists(self, name, corr):
        sorter = lambda i, j: 2 * (i.GetMaximum() < j.GetMaximum()) - 1
        good = [h.Clone('EDITED_' + corr + h.GetName()   ) for h in self.histograms if name in h.GetName() and not self.exclusion in h.GetName()]
        good.sort(sorter) 
        return good

    def Correlate(self, good, corr, corrfunc):
        if not corr: return
        mixed = [h for h in good if 'mix' in h.GetName().lower()]
        if not mixed: return None, None, None
        if len(mixed) > 1: print 'You have more than one mixed histograms'
        if not corrfunc:   print 'You are correlating when you have no correlation function "corrfunc"'
        good.remove(mixed[0])
        map(lambda x: corrfunc(x, mixed[0]), good)


    def SetBinLabels(self, histogram):
         for i in range(1, histogram.GetNbinsX() + 1):
            run = int(histogram.GetXaxis().GetBinLabel(i))
            fill = self.fill[run]
            histogram.GetXaxis().SetBinLabel(i, "%d          f%d" %(run, fill))

            
    def GetPlotData(self, name, corr='', corrfunc=None):
        good = self.FindNecessaryHists(name, corr)
        map(lambda x: x.SetMaximum(x.GetMaximum() * 1.2), good)
        map(self.SetBinLabels, good)
        # map(lambda x: x.SetLineWidth(2), good)

        self.Correlate(good, corr, corrfunc)

        titles = [h.GetTitle() for h in good]
        good_title = ' '.join(good[0].GetTitle().split()[:-1] )
        titles = [' '.join(x.split()[-2:]) for x in titles]

        self.exclusion = ' '
        return good, titles, good_title
        
    def DrawPad(self, name, exc = ' ', corr = '', mrange = None, corrfunc=lambda x, y: x.Divide(y)):
        self.exclusion = exc
        good, titles, good_title = self.GetPlotData(name, corr, corrfunc)
        if not good: return None
        good[0].SetTitle(good_title + ' ' + corr)
        good[0].GetXaxis().SetRange(good[0].FindFirstBinAbove(0, 1) , good[0].FindLastBinAbove(0, 1) )
        if mrange : good[0].GetXaxis().SetRangeUser(mrange[0], mrange[1]) 
        colors = [38, 46, 1, 30]

        map(lambda h, c: h.SetLineColor(c), good, colors)

        map(lambda x, o: x.Draw(o), good, len(good) * ['same'])

        self.legends.append(ROOT.TLegend(0.9, 0.5, 1.0, 0.8))
        legend = self.legends[-1]
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.02)

        map(lambda h, t: legend.AddEntry(h, t), good, titles)
        legend.Draw()
        ROOT.gPad.SetGridx()
        ROOT.gPad.SetGridy()

        return good

    def Draw(self, name, exc = ' ', mrange = None):
        ROOT.gStyle.SetOptStat(0)
        canvas = self.GetCanvas()
        a = self.DrawPad(name, exc, '', mrange)
        draw_and_save(name, True)
        
fill = {236137:4381, 236138:4381, 236150:4381, 236151:4381, 236153:4381, 236158:4381, 236161:4381, 236163:4381, 236204:4384, 236222:4384, 236227:4384, 236234:4384, 236238:4384, 236240:4384, 236242:4384, 236244:4384, 236246:4384, 236248:4384, 236348:4391, 236349:4391, 236352:4391, 236353:4391, 236354:4391, 236356:4391, 236359:4391, 236389:4393, 236393:4393, 236441:4398, 236443:4398, 236444:4398, 236556:4402, 236558:4402, 236562:4402, 236563:4402, 236564:4402, 236565:4402, 236813:4410, 236814:4410, 236815:4410, 236816:4410, 236821:4410, 236824:4410, 236835:4410, 236848:4410, 236850:4410, 236860:4410, 236862:4410, 236863:4410, 236866:4410 }

def main():
	mfile, drawer  = TFile('ProductionQA.hist.root'), BufferDrawer(fill)
	mlist =  mfile.GetListOfKeys()

	for hisogram in mlist: 
		h = hisogram.ReadObj()
		drawer.Update(h)

	drawer.Draw('CluEnergy')
	drawer.Draw('CluMult')
	drawer.Draw('Ncell')
	drawer.Draw('0Num')
	drawer.Draw('0Mass')
	drawer.Draw('0Sigma')

if __name__ == '__main__':
    main()
