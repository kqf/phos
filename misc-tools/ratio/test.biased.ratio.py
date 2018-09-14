import ROOT
import numpy as np


def data(a, b, size=1e6, ratio=0.9):
    data = np.random.uniform(a, b, size=int(size))
    sampled = np.random.choice(data, int(ratio * size), False)
    return data, sampled


def main():
    a, b = 1, 50
    sample, subsample = data(a, b)
    original = ROOT.TH1F("original", "Original; E GeV", 25, 0, 50)
    original.Sumw2()
    map(original.Fill, sample)
    # original.Draw()

    sampled = original.Clone()
    sampled.SetTitle("sampled")
    sampled.Sumw2()
    sampled.Reset()
    map(sampled.Fill, subsample)
    # sampled.Draw("same")

    ratio = ROOT.TGraphAsymmErrors(sampled, original)
    ratio.Draw()

    canvas = ROOT.gROOT.FindObject("c1")
    canvas.Update()
    raw_input("Press enter.")


if __name__ == "__main__":
    main()
