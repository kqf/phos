#!/usr/bin/python

import ROOT
import collections

from ptplotter import PtPlotter
from outputcreator import OutputCreator, SpectrumExtractor
from invariantmass import InvariantMass, InvariantMassNoMixing
from options import Options

from broot import BROOT as br

ROOT.TH1.AddDirectory(False)


class DataSlicer(object):
    def __init__(self, options = Options()):
        super(DataSlicer, self).__init__()
        self.opt = options.pt
        # TODO: Either replace this with factory method or configure it in pipeline
        extract = InvariantMass if self.opt.use_mixed else InvariantMassNoMixing
        self.extract_mass = lambda hists, x, y: extract(hists, x, y, options)

    @staticmethod
    def _hists(hists):
        try:
            iter(hists)
            return hists
        except TypeError:
            return hists.read()


    def transform(self, inputs):
        intervals = zip(self.opt.ptedges[:-1], self.opt.ptedges[1:])
        assert len(intervals) == len(self.opt.rebins), \
            'Number of intervals is not equal to the number of rebin parameters'

        return map(
            lambda x, y: self.extract_mass(
                self._hists(inputs), x, y
            ),
            intervals,
            self.opt.rebins
        )


class KinematicTransformer(object):

    def __init__(self, options, label):
        super(KinematicTransformer, self).__init__()
        self.opt = options.pt
        self.label = label
        self.OutType = collections.namedtuple('SpectrumAnalysisOutput', self.opt.output_order)
        self.extractor = SpectrumExtractor(self.opt.output_order)


    def histograms(self, data):
        iter_collection = zip(
            self.opt.output_order, # Ensure ordering of `data`
            zip(*data)
        )

        # Extract the data
        # Don't use format, as it confuses root/latex syntax
        output = {quant: 
            OutputCreator.output_histogram(
                quant,
                self.opt.output[quant] % self.opt.partlabel,
                self.label,
                self.opt.priority,
                self.opt.ptedges,
                d
            ) for quant, d in iter_collection
        }

        # Convert to a proper datastructure 
        return self.OutType(**output)


    def _decorate_hists(self, histograms):
        # Scale by the number of events 
        histograms.spectrum.Scale(1. / self.nevents)
        histograms.spectrum.logy = True
        histograms.npi0.logy = True
        return histograms 

        
    # TODO: Move All Serialization logic to OutputCreator
    def quantities(self, masses, draw = True):
        self.nevents = next(iter(masses)).mass.nevents
        values = map(self.extractor.eval, masses)

        # Create hitograms
        histos = self.histograms(values)
        decorated = self._decorate_hists(histos)

        if self.opt.dead_mode: 
            return decorated 

        self.plotter = PtPlotter(masses, self.opt, self.label)
        self.plotter.draw(draw)
        return decorated 

