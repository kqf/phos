from spectrum.processing import DataSlicer, PeakPropertiesEstimator
from spectrum.processing import DataExtractor, MassFitter
from spectrum.processing import InvariantMassExtractor
from spectrum.processing import InvariantMassPlotter
from spectrum.options import Options, OptionsSPMC, CompositeOptions
from spectrum.pipeline import Pipeline, ParallelPipeline, ReducePipeline
from spectrum.pipeline import AnalysisDataReader
from spectrum.pipeline import TransformerBase
import spectrum.broot as br


class SimpleAnalysis(TransformerBase):

    def __init__(self, options=Options(), plot=False):
        super(SimpleAnalysis, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ("read", AnalysisDataReader()),
            ("slice", DataSlicer(options.pt)),
            ("parametrize", InvariantMassExtractor(options.invmass)),
            ("fitmasses", MassFitter(options.invmass.use_mixed)),
            ("ranges", PeakPropertiesEstimator(options.calibration)),
            ("invmasses", InvariantMassPlotter()),
            ("data", DataExtractor(options.output))
        ])


class CompositeAnalysis(TransformerBase):

    def __init__(self, options, plot=False):
        super(CompositeAnalysis, self).__init__()
        self.mergeranges = options.mergeranges
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("analysis-{0}".format(title), Analysis(opt))
                for title, opt in options.steps
            ]),
            self.merge
        )

    def merge(self, hists, loggs):
        if len(hists) == 2:
            spectra = map(lambda x: x.spectrum, hists)
            for spec in spectra:
                bin = spec.FindBin(self.mergeranges[0][1])
                area = spec.Integral(bin - 1, bin + 1)
                if area:
                    spec.Scale(1. / area)

        truncated = [
            br.sum_trimm(obs_pt, self.mergeranges)
            for obs_pt in zip(*hists)
        ]

        # Use the same container as normal analysis
        AnalysisOutputType = type(next(iter(hists)))
        return AnalysisOutputType._make(truncated)


class Analysis(TransformerBase):

    _types = {
        Options: SimpleAnalysis,
        OptionsSPMC: SimpleAnalysis,
        CompositeOptions: CompositeAnalysis
    }

    def __init__(self, options, plot=False):
        super(Analysis, self).__init__(plot)
        Type = self._types.get(type(options))
        self.pipeline = Type(options, plot).pipeline
