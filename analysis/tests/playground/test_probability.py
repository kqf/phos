import pytest
import ROOT
import numpy as np
from spectrum.comparator import Comparator


def prob(p):
    return 0.5


def reconstruct(hist, label, weightf=lambda x, y: 1):
    reco = hist.Clone(hist.GetName() + 'Reconstructed' + label)
    reco.Reset()
    reco.label = label

    for i in range(1, hist.GetNbinsX() + 1):
        photons = np.random.randint(0, 2, (int(hist.GetBinContent(i)), 2))
        for pair in photons:
            if pair[0] and pair[1]:
                reco.Fill(hist.GetBinCenter(i), weightf(*map(prob, pair)))
    return reco


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_probability_normalization():
    nmesons = 30000
    title = '"Gnerated" (exponential distribution) #pi^{0} energy ' + \
        ' spectrum #it{N}_{#pi^{0}} = %d; E, GeV'
    hist = ROOT.TH1F('hGenerated', title % nmesons, 20, 0, 40)
    spectrumf = ROOT.TF1('pi0spectrum', 'TMath::Exp(-0.1 * x)', 0, 40)
    hist.FillRandom(spectrumf.GetName(), nmesons)
    hist.label = 'original'

    reco1 = reconstruct(hist, 'noweight')
    reco2 = reconstruct(hist, 'w1 * w2', lambda x, y: 1. / (x * y))
    reco3 = reconstruct(hist, '(w1 + w2)/2', lambda x, y: 2. / ((x + y)))

    Comparator().compare([hist, reco1, reco2, reco3])
