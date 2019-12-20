import ROOT
from contextlib import contextmanager


@contextmanager
def canvas():
    canvas = ROOT.TCanvas("canvas", "", 500, 500)
    yield canvas
    canvas.Update()
    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    ROOT.gApplication.Run(True)


@contextmanager
def tfile(filename, option="RECREATE"):
    ofile = ROOT.TFile(filename, option)
    yield ofile
    ofile.Write()
    ofile.Close()


def main():
    hist = ROOT.TH1F("invmass", "Peak distribution", 750, 0, 1.5)
    formula = "[0] + [1]*(x-{mass:.3f}) + [2]*(x-{mass:.3f})^2"
    background = ROOT.TF1("background", formula.format(mass=0.135), 0, 1.5)
    background.SetParameters(*[0.0131, -0.0016, 0])
    hist.FillRandom(background.GetHistogram(), 100000)

    signal = ROOT.TF1("signal", "gaus(0)", 0, 1.5)
    signal.SetParameters(*[0.0098, 0.1368, 0.008])
    hist.FillRandom(signal.GetHistogram(), 10000)

    # with canvas():
    #     hist.Draw()

    with tfile("data.root"):
        hist.Write()


if __name__ == '__main__':
    main()
