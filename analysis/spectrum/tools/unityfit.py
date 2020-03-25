import ROOT
import spectrum.broot as br


def unityfit(ratio, title, fit_range=(0, 100)):
    fitf = ROOT.TF1("ratio", "1. - pol0(0)", *fit_range)
    fitf.SetParameter(0, 0.0)
    ratio.Fit(fitf, "Rq")
    fitf.SetTitle("1 + #delta_{{{}}} = 1 {} {:.4f} #pm {:.4f}".format(
        ratio.GetName(),
        "+" if fitf.GetParameter(0) > 0 else "-",
        abs(fitf.GetParameter(0)),
        fitf.GetParError(0)
    ))

    sys_error = abs(fitf.GetParameter(0))
    sys_error_conf = fitf.GetParError(0)

    output = ratio.Clone()
    output.Reset()
    output.Clear()
    output.GetListOfFunctions().Add(fitf)
    output.SetName("{}_unity".format(ratio.GetName()))
    output.GetXaxis().UnZoom()
    output.SetTitle(title)
    for i in br.hrange(output):
        output.SetBinContent(i, sys_error)
        output.SetBinError(i, sys_error_conf)
    return output
