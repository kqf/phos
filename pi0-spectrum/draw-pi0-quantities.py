#!/usr/bin/python

import ROOT
import numpy as np
from math import pi
from CrystalBall import ExtractQuantities, Fit

def draw_and_save(name, draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs('results/' + name + '.pdf')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)

class PtDependent(object):
    def __init__(self, name, title, label):
        super(PtDependent, self).__init__()
        self.name = name
        self.title = title
        self.label = label

    def get_hist(self, bins, data):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))
        hist.GetXaxis().SetTitle('P_{T}, GeV/c')
        [hist.SetBinContent(i + 1, m) for i, m in enumerate(data[0])]
        [hist.SetBinError(i + 1, m) for i, m in enumerate(data[1])]
        hist.label = self.label
        return hist 

class PtAnalyzer(object):
    def __init__(self, lst, name= 'hMassPtN3', label ='N_{cell} > 3'):
        super(PtAnalyzer, self).__init__()
        self.nevents = lst.FindObject('TotalEvents').GetEntries()
        self.rawhist = lst.FindObject(name)
        self.rawmix = lst.FindObject('hMix' + name[1:])
        self.label = label

    def divide_into_bins(self, n = 20):
        # hist = self.rawhist.ProjectionY()
        # a, b, xmax, surf  = hist.FindBin(1.0001), hist.FindLastBinAbove(), hist.GetNbinsX(), int(hist.Integral() / n)
        # edges = [a]
        # for i in range(a, xmax):
            # s = hist.Integral(a, i)
            # print surf - s, hist.Integral() 
            # def compare(a, b, tol = 1.): return int(a / tol) == int(b / tol)
            # if compare(s, surf) or (surf - s) < 0:
                # a = i
                # edges.append(i)
        # edges.append(b)
        # return edges[1:]
        res = list(np.logspace(np.log10(1.) , np.log10(15), n))
        bins = map(self.rawhist.GetYaxis().FindBin, res)
        bins = sorted(set(bins))
        return bins

    def estimate_background(self, real, mixed):
        canvas = ROOT.gROOT.FindObject('c1')

        ratio = real.Clone()
        ratio.Divide(mixed)

        fitf, bckgrnd = Fit(ratio)
        canvas.Update()

        mixed.Sumw2()
        mixed.Multiply(bckgrnd)

        mixed.SetLineColor(46)

        real.Draw()
        mixed.Draw('same')
        canvas.Update()

        # if self.label != 'Mixing':raw_input()
        real.SetAxisRange(1.01 * bckgrnd.GetXmin(),  0.99 * bckgrnd.GetXmax(), "X");
        return mixed


    def extract_data(self, a, b):
        canvas = ROOT.gROOT.FindObject('c1')
        name = self.rawhist.GetName() + '_%d_%d' % (a, b)
        real, mixed = self.rawhist.ProjectionX(name, a, b), self.rawmix.ProjectionX(name + 'mix', a, b)
        real.Sumw2()


        mixed = self.estimate_background(real, mixed)
        if self.label == 'Mixing': real.Add(mixed, -1)

        lower, upper = self.rawhist.GetYaxis().GetBinCenter(a), self.rawhist.GetYaxis().GetBinCenter(b)
        real.SetTitle('%.4g < P_{T} < %.4g #events = %d' % (lower, upper, self.nevents) )
        res = ExtractQuantities(real)
        if self.label == 'Mixing': raw_input()
        return res

    def quantities(self):
        ranges = self.divide_into_bins()
        intervals = zip(ranges[:-1], ranges[1:])
        data   = np.array([self.extract_data(a, b) for a, b in intervals]).T

        histgenerators = [PtDependent('mass', '#pi^{0} mass position;;m, GeV/c^{2}', self.label),
                          PtDependent('width', '#pi^{0} peak width ;;#sigma, GeV/c^{2}', self.label),
                          PtDependent('spectrum', 'raw #pi^{0} spectrum ;;#frac{1}{2 #pi #Delta p_{T} } #frac{dN_{rec} }{dp_{T}}', self.label),  
                          PtDependent('chi2ndf', '#chi^{2} / N_{dof} (p_{T});;#chi^{2} / N_{dof}', self.label) ]

        ptedges = map(self.rawhist.GetYaxis().GetBinCenter, ranges)


        m, em, s, es, n, en, chi, echi = data

        n = [n[i] / (b - a) / (2. * pi)   for i, (a, b) in enumerate(intervals)]
        en = [en[i] / (b - a) / (2. * pi) for i, (a, b) in enumerate(intervals)]

        data = [(m, em), (s, es), (n, en), (chi, echi)]

        histos = [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(data)] 
        map(nicely_draw, histos)
        return histos


def nicely_draw(hist, option = '', legend = None):
    hist.Draw(option)

    if 'spectrum' in hist.GetName(): 
        ROOT.gPad.SetLogy()
    else:
        ROOT.gPad.SetLogy(0)

    legend = legend if legend else ROOT.TLegend(0.9, 0.4, 1.0, 0.6)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.AddEntry(hist, hist.label)
    legend.Draw('same')
    draw_and_save('xlin_' + hist.GetName(), save = True)



def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)
    mfile = ROOT.TFile('LHC16h.root')

    second = PtAnalyzer(mfile.PhysNoTender, label = 'Mixing').quantities()
    first  = PtAnalyzer(mfile.PhysNoTender, label = 'No Mixing').quantities()

    import compare as cmpr
    diff = cmpr.Comparator()
    diff.compare_lists_of_histograms(first, second)


if __name__ == '__main__':
    main()