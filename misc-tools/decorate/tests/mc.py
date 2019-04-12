import ROOT
import random


def fill_random(histogram, pars):
    if type(histogram) is ROOT.TH1F:
        return fill_random1d(histogram, pars)
    fill_random2d(histogram, pars)


def fill_random1d(histogram, pars):
    f1 = ROOT.TF1(
        'mfunc', "TMath::Exp( -1 * (x - [0]) * (x - [0]) / [1] / [1] )")
    f1.SetParameter(0, pars[0] * 2 * pars[0])
    f1.SetParameter(1, 3 - pars[1])
    histogram.FillRandom('mfunc', 10000)


def fill_random2d(histogram, pars):
    xaxis, yaxis = histogram.GetXaxis(), histogram.GetYaxis()

    def iterate(x):
        return range(1, x.GetNbins() + 1)

    for i in iterate(xaxis):
        for j in iterate(yaxis):
            histogram.SetBinContent(i, j, random.randint(1, 5))
