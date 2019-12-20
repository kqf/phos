import ROOT
from contextlib import contextmanager


def fitfunctions():
    formula = "[0] + [1]*(x-{mass:.3f}) + [2]*(x-{mass:.3f})^2"
    background = ROOT.TF1("background", formula.format(mass=0.135), 0, 1.5)
    signal = ROOT.TF1("asignal", "gaus", 0, 1.5)
    return signal, background


@contextmanager
def canvas():
    canvas = ROOT.TCanvas("canvas", "", 500, 500)
    yield canvas
    canvas.Update()
    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    ROOT.gApplication.Run(True)


def main():
    infile = ROOT.TFile.Open("data.root")
    hist = infile.invmass
    signal, background = fitfunctions()

    fitf = ROOT.TF1("func", "{}(0) + {}(3)".format(
        signal.GetName(), background.GetName()), 0., 1.5)
    print(fitf)
    fitf.SetParameters(*[0.98, 0.1368, 0.008, 0.0131, -0.0016, 0])
    with canvas():
        initial = fitf.Clone()
        initial.SetLineColor(ROOT.kOrange + 1)

        hist.Fit(fitf, "R", *[0.06, 0.22])
        hist.Draw()
        initial.Draw()


if __name__ == '__main__':
    main()
