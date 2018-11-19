import ROOT
import numpy as np
import root_numpy as rnp
import plotting
ROOT.TH1.AddDirectory(False)

filepath = "../../../neutral-meson-spectra/" \
    "input-data/data/LHC16/trigger_qa/iteration2/LHC16g-pass1.root"


def rebin(hists, n=4):
    for hist in hists:
        hist.Rebin2D(n)
    return hists


def channel_frequency(patches, name):
    trigchannels = map(rnp.hist2array, patches)
    counts = np.asarray(trigchannels).reshape(-1)
    counts = counts[counts > 0]
    freq = ROOT.TH1F(name, "Distribution of 4x4 trigger;; hits",
                     int(max(counts)), np.min(counts), np.max(counts))
    map(freq.Fill, counts)
    return freq


def channel_badmap(patches, fmin, fmax):
    trigchannels = map(rnp.hist2array, patches)
    counts = np.asarray(trigchannels)
    badmap = np.ones_like(counts)
    badmap[(fmin < counts) & (counts < fmax)] = 0
    hmaps = []
    for i, (bmap, orig) in enumerate(zip(badmap, patches)):
        hmap = orig.Clone("h4x4BadMap_mod{}".format(i))
        rnp.array2hist(bmap, hmap)
        hmaps.append(hmap)
    return hmaps


def save_maps(patches, filename="trigger-bad-map.root"):
    ofile = ROOT.TFile(filename, "recreate")
    for module in patches:
        module.Write()
    ofile.Close()


def fit_channels(patches):
    trigchannels = map(rnp.hist2array, patches)
    counts = np.asarray(trigchannels).reshape(-1)
    counts = counts[counts > 0]

    ROOT.gStyle.SetOptFit(1)
    fitf = ROOT.TF1("fgaus", "gaus(0)", 2, 40)
    fitf.SetParameter(0, 5)
    fitf.SetLineColor(ROOT.kGreen + 1)

    freq = ROOT.TH1F("freq", "Distribution of 4x4 trigger; hits", 50, 0, 50)
    map(freq.Fill, counts)
    freq.SetLineColor(ROOT.kBlue + 1)
    freq.Fit(fitf, "R")
    freq.Draw()
    plotting.decorate_pad(ROOT.gPad)
    ROOT.gPad.Update()
    raw_input()
    return fitf.GetParameter(1), fitf.GetParameter(2)


def draw_line(hist, position):
    line = ROOT.TLine(position, hist.GetMinimum(),
                      position, hist.GetMaximum())
    line.SetLineColor(1)
    line.SetLineStyle(7)
    hist.line = line
    return line


def main(nmodules=4):
    l0 = ROOT.TFile(filepath).Get("PHOSTriggerQAResultsL0")
    trigger_patches = rebin([
        l0.FindObject("h4x4SM{}".format(i))
        for i in range(1, nmodules + 1)
    ])
    matched_trigger_patches = rebin([
        l0.FindObject("h4x4CluSM{}".format(i))
        for i in range(1, nmodules + 1)
    ])
    channels = channel_frequency(trigger_patches, "all")
    matched_channels = channel_frequency(matched_trigger_patches, "matched")
    mu, sigma = fit_channels(trigger_patches)

    title = "{} good channels: {} < # hits < {}".format(
        channels.GetTitle(),
        1,
        mu + 2 * sigma
    )

    plotting.plot([
        channels,
        matched_channels,
    ], labels=["trigger patches", "matched triggers"], title=title)

    maps = channel_badmap(trigger_patches, 1, mu + 3 * sigma)
    save_maps(maps)


if __name__ == '__main__':
    main()
