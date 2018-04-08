#!/usr/bin/python

from spectrum import Spectrum
from transformer import TransformerBase
from options import EfficiencyOptions
from .input import SingleHistInput
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

class Efficiency(TransformerBase):


    def __init__(self, options=EfficiencyOptions(), recalculate=False):
        super(Efficiency, self).__init__()
        self.pipeline = RatioUnion(
            Pipeline([
                ("ReconstructMesons", Analysis(options.analysis)),
                ("NumberOfMesons", HistogramSelector("npi0"))
            ]),
            SingleHistInput(options.genname)
        )


class EfficiencyMultirange(TransformerBase):

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
