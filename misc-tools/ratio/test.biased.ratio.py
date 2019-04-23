from contextlib import contextmanager
import ROOT
import numpy as np


@contextmanager
def canvas(scale=6):
    canvas = ROOT.TCanvas("canvas", "canvas", 128 * scale, 96 * scale)
    try:
        yield canvas
    finally:
        canvas.Update()
        raw_input("Press enter...")


def data(a, b, size=1e6, ratio=0.9):
    data = np.random.uniform(a, b, size=int(size))
    sampled = np.random.choice(data, int(ratio * size), False)
    return data, sampled


def asymm_ratio(numerator, denominator):
    ratio = ROOT.TGraphAsymmErrors(numerator, denominator)
    return ratio


def main():
    a, b = 1, 50
    sample, subsample = data(a, b)
    original = ROOT.TH1F("original", "Original; E GeV", 25, 0, 50)
    original.Sumw2()
    map(original.Fill, sample)
    # original.Draw()

    sampled = original.Clone()
    sampled.SetTitle("sampled")
    sampled.Reset()
    sampled.Sumw2()
    map(sampled.Fill, subsample)

    with canvas() as cnv:
        cnv.Divide(1, 2)
        cnv.cd(1)
        original.Draw()
        sampled.Draw("same")

        cnv.cd(2)
        ratio = asymm_ratio(sampled, original)
        ratio.Draw()


if __name__ == "__main__":
    main()
