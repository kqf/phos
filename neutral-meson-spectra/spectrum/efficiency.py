#!/usr/bin/python

from spectrum import Spectrum
from options import Options
from .input import Input, read_histogram, SingleHistInput
from comparator import Comparator
from analysis import Analysis
from pipeline import Pipeline, RatioUnion, HistogramSelector, ReducePipeline, ParallelPipeline

from broot import BROOT as br

import ROOT

import os.path
import unittest


# NB: This test is to compare different efficiencies
#     estimated from different productions
#

class Efficiency(object):


    def __init__(self, options=Options(), recalculate=False):
        super(Efficiency, self).__init__()
        self.runion = RatioUnion(
            Pipeline([
                ("ReconstructMesons", Analysis(options.analysis)),
                ("NumberOfMesons", HistogramSelector("npi0"))
            ]),
            SingleHistInput(options.genname)
        )
        self.recalculate = recalculate
        self.oname = 'fixmelater.root'


    def transform(self, inputs, loggs):
        if self.recalculate:
            return self.efficiency(inputs, loggs)
        try:
            return self.read_efficiency(inputs)
        except IOError:
            return self.efficiency(inputs, loggs)


    def read_efficiency(self, inputs):
        if not os.path.isfile(self.oname):
            raise IOError('No such file: {0}'.format(self.oname))

        infile = ROOT.TFile(self.oname)
        result = infile.GetListOfKeys().At(0).ReadObj()
        result.label = inputs.label
        return result

    def efficiency(self, inputs, loggs=None):
        ratio = self.runion.transform(inputs, loggs)
        return ratio


class EfficiencyMultirange(object):

    def __init__(self, options, recalculate=True):
        super(EfficiencyMultirange, self).__init__()

        self.pipeline = ReducePipeline(
            ParallelPipeline([
                    ("efficiency-{0}".format(ranges), Efficiency(opt, recalculate))
                     for (opt, ranges) in zip(options.suboptions, options.mergeranges)
                ]
            ),
            lambda x: br.sum_trimm(x, options.mergeranges)
        )

    def transform(self, inputs, loggs):
        return self.pipeline.transform(inputs, loggs)