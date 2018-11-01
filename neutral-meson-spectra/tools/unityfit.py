import ROOT
from spectrum.broot import BROOT as br


def unityfit(ratio, newname, title, fit_range=(0, 100)):
    fitf = ROOT.TF1("ratio", "1. - pol0(0)", *fit_range)
    fitf.SetParameter(0, 0.0)
    ratio.Fit(fitf, "Rq")
    # Comparator().compare(ratio)

    sys_error = abs(fitf.GetParameter(0))
    sys_error_conf = fitf.GetParError(0)

    output = ratio.Clone(newname)
    output.Reset()
    output.SetTitle(title)
    for i in br.range(output):
        output.SetBinContent(i, sys_error)
        output.SetBinError(i, sys_error_conf)
    return output
