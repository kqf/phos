from processing import DataSlicer, RangeEstimator, DataExtractor, MassFitter
from processing import InvariantMassExtractor
from options import Options, CompositeOptions
from pipeline import Pipeline, ParallelPipeline, ReducePipeline
from pipeline import TransformerBase
from broot import BROOT as br


class SimpleAnalysis(TransformerBase):

    def __init__(self, options=Options(), plot=False):
        super(SimpleAnalysis, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ("slice", DataSlicer(options.pt)),
            ("parametrize", InvariantMassExtractor(options.invmass)),
            ("fitmasses", MassFitter(options.invmass.use_mixed)),
            ("ranges", RangeEstimator(options.spectrum)),
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

        # Transpose
        pairs = zip(*hists)

        truncated = [
            br.sum_trimm(obs_pt, self.mergeranges)
            for obs_pt in pairs
        ]

        # Use the same container as normal analysis
        # TODO: Fix me!
        results = hists[0]._make(truncated)
        loggs.update({"composite_output": results._asdict()})
        return results


class Analysis(TransformerBase):

    _types = {
        Options: SimpleAnalysis,
        CompositeOptions: CompositeAnalysis
    }

    def __init__(self, options, plot=False):
        super(Analysis, self).__init__(plot)
        Type = self._types.get(type(options))
        self.pipeline = Type(options, plot).pipeline
