import ROOT
import numpy as np
import root_numpy as rnp

filepath = "../../../neutral-meson-spectra/" \
    "input-data/data/LHC16/trigger_qa/iteration2/LHC16g-pass1.root"


def rebin(hists, n=4):
    for hist in hists:
        hist.Rebin2D(n)
    return hists


def main(nmodules=4):
    l0 = ROOT.TFile(filepath).Get("PHOSTriggerQAResultsL0")
    l0.ls()
    patches = [
        l0.FindObject("h4x4SM{}".format(i))
        for i in range(1, nmodules + 1)
    ]
    rebin(patches)
    trigchannels = map(rnp.hist2array, patches)
    channel_counts = np.asarray(trigchannels).reshape(-1)
    channel_counts = channel_counts[channel_counts > 0]
    freq = ROOT.TH1F("freq", "", len(channel_counts), 0, len(channel_counts))
    map(freq.Fill, channel_counts)
    freq.Draw()
    raw_input()


if __name__ == '__main__':
    main()
