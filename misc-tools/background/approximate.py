import ROOT

FILE = "../../neutral-meson-spectra/input-data/data/LHC16/corrected/LHC16.root"


def wait(logy=True):
    canvas = ROOT.gROOT.FindObject("c1")
    canvas.SetLogy(logy)
    canvas.Update()
    raw_input()


def approximate(mixing):
    func = ROOT.TF2(
        "func",
        "([0] * TMath::Exp([1] * x[1])"
        "+[2] * TMath::Exp([3] * x[1])"
        "+[4] * TMath::Exp([5] * x[1])) * "
        "[6] * TMath::Exp([7] * x[0])", 0, 1.5, 4, 20)
    func.SetParameter(0, 1.76156e+01)
    func.SetParameter(1, -1.75769e+00)
    func.SetParameter(2, 1.24408e+01)
    func.SetParameter(3, -1.75770e+00)
    func.SetParameter(4, 1.15755e+01)
    func.SetParameter(5, -5.12771e-01)
    func.SetParameter(6, 1.46215e+01)
    func.SetParameter(7, -5.66055e+00)
    mixing.Fit(func, "R")
    mixing.Draw("lego")
    func.Draw("lego same")
    print(func.GetChisquare() / func.GetNDF())
    wait(False)


def approximate_pt(mixing):
    func = ROOT.TF1('pt', "expo(0) + expo(2) + expo(4)", 1, 20)
    func.SetParameter(0, 1.76156e+01)
    func.SetParameter(1, -1.75769e+00)
    func.SetParameter(2, 1.24408e+01)
    func.SetParameter(3, -1.75770e+00)
    func.SetParameter(4, 1.15755e+01)
    func.SetParameter(5, -5.12771e-01)
    pt = mixing.ProjectionY()
    pt.Fit(func, "R")
    pt.Draw()
    wait()


def approximate_mass(mixing):
    func = ROOT.TF1('mass', "expo(0)", 0.2, 1.5)
    mass = mixing.ProjectionX()
    mass.Fit(func, "R")
    mass.Draw()
    wait()


def main():
    infile = ROOT.TFile(FILE)
    mixing = infile.Get("Phys").FindObject("hMixMassPt")

    # approximate_pt(mixing)
    # approximate_mass(mixing)
    approximate(mixing)


if __name__ == '__main__':
    main()
