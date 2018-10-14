#!/usr/bin/python

import ROOT
import unittest

from spectrum.input import read_histogram
from spectrum.sutils import wait
import re


class Efficiency(unittest.TestCase):

    def setUp(self):
        # self.particles = [-3322, -3222, -3214, -3122, -2214, -2114, -511, -423, -421, -411, -323, -313, -213, 1, 2, 3, 4, 5, 21, 213, 221, 223, 310, 313, 323, 331, 333, 411, 421, 423, 445, 1103, 2101, 2103, 2112, 2114, 2203, 2214, 3122, 3214, 3222, 3322]
        # self.particles = [-213, -211, 211, 213, 221, 223, 310, 3122]
        self.particles = [1, 2, 3, 4, -313, -213,
                          221, 323, 21, 310, 313, 223, -323, 213]
        self.known_particles = 'Xi', 'Sigma', 'Lambda', 'Delta', 'rho', 'omega', 'eta', 'phi', 'pi'

    # @unittest.skip('')
    def testConvert(self):
        def fname(x):
            return ROOT.TParticle(x, *[0] * 13).GetName()
        names = {p: fname(p) for p in self.particles}
        # print names

        names = {self.transform(names[p]): p for p in names}
        hist = ROOT.TH1F('data', 'data', len(names), 0, len(names))
        for i, n in enumerate(names):
            hist.GetXaxis().SetBinLabel(i + 1, n)

        print names

        hist.Draw()
        hist.FillRandom("gaus")
        wait()

    def transform(self, name):
        for s in re.findall(r"[^a-zA-Z_]", name):
            name = name.replace(s, '^{' + s + '}')

        if '_bar' in name:
            name = name.replace('_bar', '')
            name = '#bar' + name

        # print name

        for k in self.known_particles:
            if k in name:
                name = name.replace(k, '#' + k)
        # print name

        if '_' in name:
            idx = name.find('_')
            name = name.replace(name[idx:], '_{' + name[idx + 1:] + '}')

        # print name

        return name

    def testExtract(self):
        ifile = 'input-data/Pythia-LHC16-a1.root'
        cprimary = 'hMC_#pi^{0}_sources_primary', 'primary cut'
        csecondary = 'hMC_#pi^{0}_sources_secondary', 'secondary cut'

        nprimary = 'hMC_#pi^{0}_sources_nocut_primary', 'primary'
        nsecondary = 'hMC_#pi^{0}_sources_nocut_secondary', 'secondary'

        def get_codes(name, label):
            hist = read_histogram(
                ifile, 'MCStudyOnlyTender', name, label=label)
            codes = map(int, [
                hist.GetBinCenter(i) - 0.5
                for i in range(1, hist.GetNbinsX() + 1)
                if hist.GetBinContent(i) > 0]
            )
            return codes

        print nprimary[1], get_codes(*nprimary)
        print nsecondary[1], get_codes(*nsecondary)

        print cprimary[1], get_codes(*cprimary)
        print csecondary[1], get_codes(*csecondary)
