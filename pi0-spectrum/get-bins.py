#!/usr/bin/python2

import ROOT
import numpy as np

def draw_and_save(name, draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs('results/' + name + '.pdf')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)

class PtDep(object):
    def __init__(self, name, title, ylabel, xlabel = 'P_{T}, GeV/c'):
        super(PtDep, self).__init__()
        self.name = name
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def get_hist(self, bins, data):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))
        hist.GetXaxis().SetTitle(self.xlabel)
        hist.GetYaxis().SetTitle(self.ylabel)
        [hist.SetBinContent(i + 1, m) for i, m in enumerate(data[0])]
        [hist.SetBinError(i + 1, m) for i, m in enumerate(data[1])]
        return hist 



# 1 (219 , 86  , 178 )
# 2 (160 , 86  , 219 )
# 3 (86  , 111 , 219 )
# 4 (86  , 211 , 219)
# 5 (86   , 219 , 127 )
# 6 (145 , 219 , 86  )
# 7 (219 , 194 , 86  )
# 8 (219 , 94  , 86  )
          


def Fit(h = None, emin = 0.05, emax = 0.3, rebin = 1):
    # Fits the pi0 peak with crystal ball + pol2,
    # fills number of pi0s, mass, width and their errors.

    if (not h) or (h.GetEntries() == 0): return;
    if rebin > 1: h.Rebin(rebin);
    h.GetXaxis().SetTitle('M_{#gamma#gamma}, GeV')
    ROOT.gStyle.SetOptFit()

    # crystal ball parameters (fixed by hand for EMCAL); TODO: PHOS parameters?
    alpha = 1.1;  # alpha >= 0
    n = 2.;       # n > 1

    # CB tail parameters
    a = ROOT.TMath.Exp(-alpha * alpha / 2.) * (n / alpha) ** n 
    b = n / alpha - alpha;

    # signal (crystal ball);
    signal = ROOT.TF1("cball", "(x-[1])/[2] > -%f ? [0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2])) : [0]*%f*(%f-(x-[1])/[2])^(-%f)" % (alpha, a, b, n) );

    # background
    background = ROOT.TF1("mypol2", "[0] + [1]*(x-0.135) + [2]*(x-0.135)^2", emin, emax);

    # signal + background
    fitfun = ROOT.TF1("fitfun", "cball + mypol2", emin, emax);
    fitfun.SetParNames("A", "M", "#sigma", "a_{0}", "a_{1}", "a_{2}");
    fitfun.SetLineColor(ROOT.kRed);
    fitfun.SetLineWidth(2);

    # make a preliminary fit to estimate parameters
    ff = ROOT.TF1("fastfit", "gaus(0) + [3]");
    ff.SetParLimits(0, 0., h.GetMaximum()*1.5);
    ff.SetParLimits(1, 0.1, 0.2);
    ff.SetParLimits(2, 0.004,0.030);
    ff.SetParameters(h.GetMaximum()/3., 0.135, 0.010, 0.);
    h.Fit(ff, "0QL", "", 0.105, 0.165);

    fitfun.SetParLimits(0, 0., h.GetMaximum()*1.5);
    fitfun.SetParLimits(1, 0.12, 0.15);
    fitfun.SetParLimits(2, 0.004,0.030);
    fitfun.SetParameters(ff.GetParameter(0), ff.GetParameter(1), ff.GetParameter(2), ff.GetParameter(3));
    h.Fit(fitfun,"QLR", "");

    # integral value under crystal ball with amplitude = 1, sigma = 1
    # (will be sqrt(2pi) at alpha = infinity)
    nraw11 = a * pow(b + alpha, 1. - n) / (n - 1.) + ROOT.TMath.Sqrt(ROOT.TMath.Pi() / 2.) * ROOT.TMath.Erfc( -alpha / ROOT.TMath.Sqrt(2.));

    # calculate pi0 values
    mass = fitfun.GetParameter(1);
    emass = fitfun.GetParError(1);

    sigma = fitfun.GetParameter(2);
    esigma = fitfun.GetParError(2);

    A = fitfun.GetParameter(0);
    eA = fitfun.GetParError(0);

    nraw = nraw11 * A * sigma / h.GetBinWidth(1);
    enraw = nraw * (eA / A + esigma / sigma);
    h.Draw()
    draw_and_save(h.GetName(), draw=False, save=True)
    return mass, emass, sigma, esigma, nraw, enraw


def get_my_list(fname='AnalysisResults.root'):
    mfile = ROOT.TFile(fname)
    mlist = mfile.Phys
    mlist.ls()
    return mlist

def compare(a, b, tol = 1):
    return int(a / tol) == int(b / tol)


def divide_into_bins(hist, n = 30):
    a, b, xmax, surf  = hist.FindFirstBinAbove(), hist.FindLastBinAbove(), hist.GetNbinsX(), int(hist.Integral() / n)
    edges = [a]
    for i in range(a, xmax):
        s = hist.Integral(a, i)
        # print surf - s, hist.Integral() 
        if compare(s, surf) or (surf - s) < 0:
            a = i
            edges.append(i)
    edges.append(b)
    return edges

def extract_data(rawhist, pt, a, b, nevents):
    name = rawhist.GetName() + '_%d_%d' % (a, b)
    hist = rawhist.ProjectionX(name, a, b)
    lower, upper = pt.GetBinCenter(a), pt.GetBinCenter(b)
    hist.SetTitle('%.4g < P_{T} < %.4g #events = %d' % (lower, upper, nevents) )
    return Fit(hist)

def get_pi0_stats(rawhist, nevents):
    pt = rawhist.ProjectionY()
    ranges = divide_into_bins(pt)
    data   = np.array([extract_data(rawhist, pt, a, b, nevents) for a, b in zip(ranges[:-1], ranges[1:])]).T

    nc = rawhist.GetName()[-1] # ncells
    histgenerators = [PtDep('mass' + nc, '#pi^{0} mass position', 'm, GeV'), PtDep('width' + nc, '#pi^{0} peak width ', '#sigma, GeV'), PtDep('amount' + nc, '#pi^{0} amount ', 'dN_{rec}/dp_{T}') ]
    ptedges = map(pt.GetBinCenter, ranges)
    m, em, s, es, n, en = data
    data = [(m, em), (s, es), (n, en)]
    return [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(data)]

def nicely_draw(histos, labels, colors):
    n = len(histos) - 1
    map(lambda x, y: x.Draw(y), histos, [''] + n * ['same'])

    if 'amount' in histos[0].GetName(): 
        ROOT.gPad.SetLogy()
        # ROOT.gPad.SetLogx(False)
    else:
        ROOT.gPad.SetLogx()


    map(lambda x, y: x.SetLineColor(y), histos, colors)
    legend = ROOT.TLegend(0.9, 0.4, 1.0, 0.6)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    map(lambda h, l: legend.AddEntry(h, l), histos, labels)
    legend.Draw('same')
    draw_and_save('xlin_' + histos[0].GetName(), save = True)
    # draw_and_save('xlog_' + histos[0].GetName(),)


def main():
    canvas = ROOT.TCanvas('c1', 'Canvas', 1000, 500)
    lst = get_my_list()
    nevetns = lst.FindObject('TotalEvents').GetEntries()
    names = ['hMassPtN3', 'hMassPtN4', 'hMassPtN5'][0:1]
    labels = [' N_{cell} > ' + str(i) for i in range(2, 5)][0:1]
    colors = [46, 38, 8][0:1]
    rawhists = [lst.FindObject(n) for n in names]
    histos = [get_pi0_stats(r, nevetns) for r in rawhists]
    histos = map(list, zip(*histos))
    print histos
    for quantity in histos:
        nicely_draw(quantity, labels, colors)


if __name__ == '__main__':
    main()