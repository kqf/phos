from __future__ import print_function

import ROOT
import numpy as np
import plotting

try:
    import root_numpy as rnp
except ValueError:
    import utils as rnp

from utils import select_tru

ROOT.TH1.AddDirectory(False)
# ROOT.gStyle.SetOptStat(0)


def plot_matrix(matrix, hist):
    hist = rnp.array2hist(matrix, hist)
    hist.Draw("colz")
    ROOT.gPad.Update()
    raw_input()


def rebin(hists, n=4):
    for hist in hists:
        hist.Rebin2D(n)
    return hists


def load_channels_multiruns(filepath, pattern, nmodules=4):
    total = []
    file = ROOT.TFile(filepath)
    for key in file.GetListOfKeys():
        l0 = key.ReadObj()
        modules = rebin([
            l0.FindObject(pattern.format(i))
            for i in range(1, nmodules + 1)
        ])
        total.append(modules)
    return total


def module_hists_to_matrix(hists):
    return np.array([map(rnp.hist2array, modules) for modules in hists])


def channel_frequency(triggers, name):
    counts = np.asarray(triggers).reshape(-1)
    counts = counts[counts > 0]
    freq = ROOT.TH1F(name, "Distribution of 4x4 trigger;; hits",
                     int(max(counts)), np.min(counts), np.max(counts))
    map(freq.Fill, counts)
    return freq


def channel_badmap(hists, triggers, fmin, fmax):
    counts = np.asarray(triggers)
    badmap = np.ones_like(counts)
    badmap[(fmin < counts) & (counts < fmax)] = 0
    hmaps = []
    for i, (bmap, orig) in enumerate(zip(badmap, hists)):
        hmap = orig.Clone("h4x4BadMap_mod{}".format(i))
        rnp.array2hist(bmap, hmap)
        hmaps.append(hmap)
    return hmaps


def save_maps(patches, filename="trigger-bad-map.root"):
    ofile = ROOT.TFile(filename, "recreate")
    for module in patches:
        module.Write()
    ofile.Close()


def fit_channels(triggers, sm, tru):
    counts = np.asarray(triggers).reshape(-1)
    counts = counts[counts > 0]

    ROOT.gStyle.SetOptFit(1)
    fitf = ROOT.TF1(
        "fpoisson",
        "[1] * TMath::Poisson(x[0], [0])", 0, 40)
    fitf.SetParameter(0, 5)
    fitf.SetParameter(1, 1000)
    fitf.SetLineColor(ROOT.kGreen + 1)
    filename = "sm{} tru{}".format(sm, tru)
    title = "Distribution of 4x4 trigger {}; cells".format(filename)
    freq = ROOT.TH1F("freq", title, 50, 0, 50)
    map(freq.Fill, counts)
    freq.SetLineColor(ROOT.kBlue + 1)
    freq.Fit(fitf, "R")
    freq.Draw()
    plotting.decorate_pad(ROOT.gPad)
    ROOT.gPad.Update()
    ROOT.gPad.SaveAs("fitted-{}.pdf".format(filename.replace(" ", "-")))
    return fitf.GetParameter(0), fitf.GetParameter(0)


def draw_line(hist, position):
    line = ROOT.TLine(position, hist.GetMinimum(),
                      position, hist.GetMaximum())
    line.SetLineColor(1)
    line.SetLineStyle(7)
    hist.line = line
    return line


def channels(thists, mhists):
    triggers = map(rnp.hist2array, thists)
    mtriggers = map(rnp.hist2array, mhists)

    channels = channel_frequency(triggers, "frequencies")
    matched_channels = channel_frequency(mtriggers, "matched")
    mu, sigma = fit_channels(triggers)

    title = "{} good channels: {} < # hits < {}".format(
        channels.GetTitle(), 1, mu + 3 * (sigma ** 0.5)
    )

    plotting.plot([
        channels,
        matched_channels,
    ], labels=["trigger patches", "matched triggers"], title=title)

    maps = channel_badmap(thists, triggers, 1, mu + 3 * sigma)
    save_maps(maps)


def channels_tru(histograms, n_trus=8):
    trigger_patches = map(rnp.hist2array, histograms)
    for sm_index, patches in enumerate(trigger_patches):
        for itru in range(1, n_trus + 1):
            tru = select_tru(patches, itru)
            plot_matrix(tru, histograms[0])
            filename = "sm{} tru{}".format(sm_index + 1, itru)
            mu, sigma = fit_channels(tru, filename)
            title = "{} good channels: {} < # hits < {}".format(
                "TRU", 1, mu + 3 * (sigma ** 0.5)
            )
            print(title)


def extract_bad_channels(data, hists, n_trus=8):
    data = np.moveaxis(data, 0, -1)
    maps = []
    for sm_index, patches in enumerate(data):
        bad_sm = np.zeros_like(patches)
        for itru in range(1, n_trus + 1):
            tru = select_tru(patches, itru)
            mu, sigma = fit_channels(tru, sm_index + 1, itru)
            bad = (tru < 0) | (tru > mu + 3 * (sigma ** 0.5))
            bad_sm += bad

        # Select only the worst channels
        bad_module = bad_sm.sum(axis=-1) > 0.1 * bad_sm.shape[-1]
        maps.append(bad_module)

    badmap = [rnp.array2hist(matrix, hist)
              for matrix, hist in zip(maps, hists)]
    save_maps(badmap)
    return maps


def channels_tru_period(filepath, n_trus=8):
    thists = load_channels_multiruns(filepath, "h4x4SM{}")
    data = module_hists_to_matrix(thists)
    extract_bad_channels(data, thists[-1], n_trus=8)


def channels_tru_total(filepaths):
    total_hists = [load_channels_multiruns(period, "h4x4SM{}")
                   for period in filepaths]
    thists = sum(total_hists, [])
    data = module_hists_to_matrix(thists)
    extract_bad_channels(data, thists[-1])
