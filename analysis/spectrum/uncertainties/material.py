import array
import ROOT
from spectrum.options import Options
from spectrum.pipeline import TransformerBase
import spectrum.broot as br


def material_budget_data():
    # There's no data required
    pass


class MaterialBudgetOptions(object):

    def __init__(self, particle="#pi^{0}"):
        super(MaterialBudgetOptions, self).__init__()
        self.edges = Options(particle).pt.ptedges
        self.title = "; #it{p}_{T} (GeV/#it{c}) ;relative sys. uncertainty"
        # The value borrowed from the 5 TeV analysis
        self.uncertainty_value = 0.02


class MaterialBudget(TransformerBase):
    def __init__(self, options, plot=False):
        self.options = options

    def transform(self, data, loggs):
        if data is not None:
            raise IOError("The input should be empty")
        edges = array.array('d', self.options.edges)
        uncertainty = ROOT.TH1F("material_budget",
                                self.options.title,
                                len(edges) - 1,
                                edges)
        for i in br.hrange(uncertainty):
            uncertainty.SetBinContent(i, self.options.uncertainty_value)
        uncertainty.label = "material budget"
        return uncertainty
