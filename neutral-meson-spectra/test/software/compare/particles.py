import ROOT
import json

import sys


class Particles(object):

    def __init__(self):
        super(Particles, self).__init__()

    def config(self):
        with open('config/test_particles.json') as f:
            particles = json.load(f)
        data = [self._spectrum(i, *particles[i]) for i in particles]

        for hist in data:
            hist.logy = 1

        discover = 'discover' in sys.argv
        compare = 'test.software.compare' in sys.argv
        skip = discover and not compare

        return data, not skip

    @staticmethod
    def _spectrum(name, a, b, par):
        from spectrum.sutils import tsallis
        function = ROOT.TF1('f' + name, lambda x,
                            p: tsallis(x, p, a, a), 0.3, 15, 3)
        function.SetParameters(*par)
        title = '%s p_{T} spectrum; p_{T}, GeV/c; #frac{dN}{dp_{T}}' % name
        histogram = ROOT.TH1F(name + '_spectrum', title, 100, 0.3, 15)
        histogram.FillRandom('f' + name, 1000000)
        histogram.label = name
        histogram.Sumw2()
        return histogram
