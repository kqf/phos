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


def channel_frequency(patches):
    trigchannels = map(rnp.hist2array, patches)
    counts = np.asarray(trigchannels).reshape(-1)
    counts = counts[counts > 0]
    freq = ROOT.TH1F("freq", "",
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
    channels = channel_frequency(trigger_patches)
    matched_channels = channel_frequency(matched_trigger_patches)

    plotting.plot([
        channels,
        matched_channels,
    ], labels=["trigger patches", "matched triggers"])

    maps = channel_badmap(trigger_patches, 1, 16)
    save_maps(maps)


if __name__ == '__main__':
    main()
