from __future__ import print_function
from contextlib import contextmanager
import ROOT
import numpy as np


def std_ratio(a, b, option="B"):
    ratio = a.Clone('ratio' + a.GetName())
    ratio.Divide(a, b, 1, 1, option)
    if not ratio.GetSumw2N():
        ratio.Sumw2()
    return ratio


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
    edges, contents = [], []
    x, y = ROOT.Double(0), ROOT.Double(0)
    for i in range(ratio.GetN()):
        ratio.GetPoint(i, x, y)
        xe = ratio.GetErrorX(i)
        ye = ratio.GetErrorY(i)
        edges.append(x - xe)
        contents.append([float(y), float(ye)])

    edges.append(x + xe)

    hist = ROOT.TH1F(
        "asym_ratio_{}".format(numerator.GetName()),
        numerator.GetTitle(),
        len(edges) - 1,
        np.array(edges)
    )
    hist.Sumw2()
    for i, (y, y_err) in enumerate(contents):
        hist.SetBinContent(i + 1, y)
        hist.SetBinError(i + 1, y_err)

    return hist


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
        ratio_asymm = asymm_ratio(sampled, original)
        ratio_asymm.SetLineColor(ROOT.kRed + 1)
        ratio_asymm.Draw()

        ratio = std_ratio(sampled, original)
        ratio.SetLineColor(ROOT.kBlue + 1)
        ratio.Draw("same")


if __name__ == "__main__":
    main()
