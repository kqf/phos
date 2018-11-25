import ROOT

# Configure ROOT
ROOT.gErrorIgnoreLevel = ROOT.kFatal


def repr1d(htype):
    def htext(self):
        name, title = self.GetName(), self.GetTitle()
        nbins = self.GetNbinsX()
        nstart = self.GetXaxis().GetBinLowEdge(1)
        nstop = self.GetXaxis().GetBinUpEdge(nbins)
        msg = '{}("{}", "{}", {}, {}, {})'
        return msg.format(htype, name, title, nbins, nstart, nstop)
    return htext


ROOT.TH1F.__repr__ = repr1d("TH1F")
ROOT.TH1D.__repr__ = repr1d("TH1D")
