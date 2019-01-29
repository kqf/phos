import ROOT
import numpy as np
import plotting
try:
    import root_numpy as rnp
except ValueError:
    import utils as rnp

ROOT.TH1.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)


def rebin(hists, n=4):
    for hist in hists:
        hist.Rebin2D(n)
    return hists


def load_channels(filepath, pattern, nmodules=4):
    l0 = ROOT.TFile(filepath).Get("PHOSTriggerQAResultsL0")
    modules = rebin([
        l0.FindObject(pattern.format(i))
        for i in range(1, nmodules + 1)
    ])
    return modules, map(rnp.hist2array, modules)


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


def fit_channels(triggers):
    counts = np.asarray(triggers).reshape(-1)
    counts = counts[counts > 0]

    ROOT.gStyle.SetOptFit(1)
    fitf = ROOT.TF1(
        "fpoisson",
        "[1] * TMath::Poisson(x[0], [0])", 0, 40)
    fitf.SetParameter(0, 5)
    fitf.SetParameter(1, 1000)
    fitf.SetLineColor(ROOT.kGreen + 1)

    freq = ROOT.TH1F("freq", "Distribution of 4x4 trigger; hits", 50, 0, 50)
    map(freq.Fill, counts)
    freq.SetLineColor(ROOT.kBlue + 1)
    freq.Fit(fitf, "R")
    freq.Draw()
    plotting.decorate_pad(ROOT.gPad)
    ROOT.gPad.Update()
    ROOT.gPad.SaveAs("fitted.pdf")
    raw_input()
    return fitf.GetParameter(1), fitf.GetParameter(2)


def draw_line(hist, position):
    line = ROOT.TLine(position, hist.GetMinimum(),
                      position, hist.GetMaximum())
    line.SetLineColor(1)
    line.SetLineStyle(7)
    hist.line = line
    return line


def channels(filepath, nmodules=4):
    hists, triggers = load_channels(filepath, "h4x4SM{}")
    mhists, matched_triggers = load_channels(filepath, "h4x4CluSM{}")

    channels = channel_frequency(triggers, "frequencies")
    matched_channels = channel_frequency(matched_triggers, "matched")
    mu, sigma = fit_channels(triggers)

    title = "{} good channels: {} < # hits < {}".format(
        channels.GetTitle(), 1, mu + 3 * (sigma ** 0.5)
    )

    plotting.plot([
        channels,
        matched_channels,
    ], labels=["trigger patches", "matched triggers"], title=title)

    maps = channel_badmap(hists, triggers, 1, mu + 3 * sigma)
    save_maps(maps)


def channels_tru(filepath, nmodules=4, ntrus=8):
    trigger_patches = load_channels(filepath, "h4x4SM{}")
    for sm_index, patches in enumerate(trigger_patches):
        for tru in range(1, ntrus):
            pass

            # channels = channel_frequency(trigger_patches, "frequencies")
            # matched_channels = channel_frequency(matched_trigger_patches, "matched")
            # mu, sigma = fit_channels(trigger_patches)

            # title = "{} good channels: {} < # hits < {}".format(
            #     channels.GetTitle(), 1, mu + 3 * (sigma ** 0.5)
            # )

            # plotting.plot([
            #     channels,
            #     matched_channels,
            # ], labels=["trigger patches", "matched triggers"], title=title)

            # maps = channel_badmap(trigger_patches, 1, mu + 3 * sigma)
            # save_maps(maps)


if __name__ == '__main__':
    channels()
