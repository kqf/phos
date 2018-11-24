import ROOT

# Configure ROOT
ROOT.gErrorIgnoreLevel = ROOT.kFatal


def repr1d(self):
    name, title = self.GetName(), self.GetTitle()
    nbins = self.GetNbinsX()
    nstart = self.GetXaxis().GetBinLowEdge(1)
    nstop = self.GetXaxis().GetBinUpEdge(nbins)
    msg = 'TH1F("{}", "{}", {}, {}, {})'
    return msg.format(name, title, nbins, nstart, nstop)


ROOT.TH1F.__repr__ = repr1d
