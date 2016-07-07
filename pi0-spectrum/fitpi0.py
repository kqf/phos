#!/usr/bin/python

import ROOT

def Fit(h = None, emin = 0.05, emax = 0.3, rebin = 1):
    # Fits the pi0 peak with crystal ball + pol2,
    # fills number of pi0s, mass, width and their errors.

    if (not h) or (h.GetEntries() == 0): return;
    if rebin > 1: h.Rebin(rebin);

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

def main():
    Fit()




    if __name__ == '__main__':
        main()