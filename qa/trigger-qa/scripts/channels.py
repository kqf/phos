import ROOT
import numpy as np
import root_numpy as rnp
import plotting

filepath = "../../../neutral-meson-spectra/" \
    "input-data/data/LHC16/trigger_qa/iteration2/LHC16g-pass1.root"


def rebin(hists, n=4):
    for hist in hists:
        hist.Rebin2D(n)
    return hists


def channel_frequency(patches):
    rebin(patches)
    trigchannels = map(rnp.hist2array, patches)
    counts = np.asarray(trigchannels).reshape(-1)
    counts = counts[counts > 0]
    # counts = (counts - np.mean(counts)) / np.std(counts)
    freq = ROOT.TH1F("freq", "",
                     int(max(counts)), np.min(counts), np.max(counts))
    map(freq.Fill, counts)
    return freq


def main(nmodules=4):
    l0 = ROOT.TFile(filepath).Get("PHOSTriggerQAResultsL0")
    l0.ls()
    trigger_patches = [
        l0.FindObject("h4x4SM{}".format(i))
        for i in range(1, nmodules + 1)
    ]
    matched_trigger_patches = [
        l0.FindObject("h4x4CluSM{}".format(i))
        for i in range(1, nmodules + 1)
    ]
    channels = channel_frequency(trigger_patches)
    matched_channels = channel_frequency(matched_trigger_patches)

    plotting.plot([
        channels,
        matched_channels,
    ], labels=["trigger patches", "matched triggers"])


if __name__ == '__main__':
    main()
