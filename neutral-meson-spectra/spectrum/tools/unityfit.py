import ROOT
from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase


def unityfit(ratio, title, fit_range=(0, 100)):
    print(ratio)
    fitf = ROOT.TF1("ratio", "1. - pol0(0)", *fit_range)
    fitf.SetParameter(0, 0.0)
    ratio.Fit(fitf, "Rq")
    # Comparator().compare(ratio)

    sys_error = abs(fitf.GetParameter(0))
    sys_error_conf = fitf.GetParError(0)

    output = ratio.Clone("{}_unity".format(ratio.GetName()))
    output.Reset()
    output.SetTitle(title)
    for i in br.range(output):
        output.SetBinContent(i, sys_error)
        output.SetBinError(i, sys_error_conf)
    return output


class UnityFitTransformer(TransformerBase):
    def __init__(self, title, fit_range):
        self.title = title
        self.fit_range = fit_range

    def transform(self, hists, loggs):
        return [unityfit(h, self.title, self.fit_range) for h in hists]