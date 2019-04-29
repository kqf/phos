from contextlib import contextmanager
import ROOT


@contextmanager
def draw_canvas(scale=6):
    canvas = ROOT.TCanvas("canvas", "canvas", 128 * scale, 96 * scale)
    try:
        yield canvas
    finally:
        canvas.Update()
        raw_input("Press enter...")


def bincenterf(hist, isxaxis=True):
    axis = hist.GetXaxis() if isxaxis else hist.GetYaxis()
    return lambda x: axis.FindBin(x)


def area_and_error(hist, a, b):
    if a == b:
        return 0, 0
    area, areae = ROOT.Double(), ROOT.Double()
    bin = bincenterf(hist)
    area = hist.IntegralAndError(bin(a), bin(b), areae)
    return area, areae


def main():
    data = ROOT.TH1F("hist", "hist", 200, -6, 6)
    data.FillRandom("gaus")

    with draw_canvas():
        data.Draw("same")
        print("Data: ", area_and_error(data, -2, 2))

        data_cloned = data.Clone()
        print("Data: ", area_and_error(data_cloned, -2, 2))

        data_cloned.Rebin(2)
        print("Data: ", area_and_error(data_cloned, -2, 2))
        data_cloned.Draw("same")


if __name__ == '__main__':
    main()
