#!/usr/bin/python

import ROOT
import test.check_default
import numpy as np


class CheckProbability(test.check_default.CheckDefault):

    def setUp(self):
        super(CheckProbability, self).setUp()
        nmesons = 20000
        self.hist = ROOT.TH1F(
            'hGenerated',
            '"Gnerated" (exponential distribution) #pi^{0} energy spectrum N_{#pi^{0}} = %d; E, GeV' % nmesons, 20, 0, 20)
        # f1 = ROOT.TF1('pi0spectrum', 'TMath::Exp(-0.1 * x)', 0, 20)
        self.hist.FillRandom('pi0spectrum', nmesons)
        self.hist.label = 'original'

    def prob(self, p):
        return 0.5

    def reconstruct(self, hist, label, w=lambda x, y: 1):
        reco = hist.Clone(hist.GetName() + 'Reconstructed' + label)
        reco.Reset()
        reco.label = label

        for i in range(1, hist.GetNbinsX() + 1):
            photons = np.random.randint(0, 2, (hist.GetBinContent(i), 2))
            for pair in photons:
                if pair[0] and pair[1]:
                    reco.Fill(hist.GetBinCenter(i), w(*map(self.prob, pair)))
        return reco

    def testProbability(self):
        reco1 = self.reconstruct(self.hist, 'noweight')
        reco2 = self.reconstruct(self.hist, 'w1 * w2',
                                 lambda x, y: 1. / (x * y))
        reco3 = self.reconstruct(
            self.hist, '(w1 + w2)/2', lambda x, y: 1. / ((x + y) / 2.))
        self.results = [[self.hist], [reco1], [reco2], [reco3]]
