from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.input import SingleHistInput
from spectrum.broot import BROOT as br


class EpSlicer(TransformerBase):

    def __init__(self, options, plot):
        super(EpSlicer, self).__init__(plot)
        self.options = options

    def transform(self, data, loggs):
        hists = [
            br.project_range(data, '_%d_%d', *rr)
            for rr in zip(self.options.ptedges[:-1], self.options.ptedges[1:])
        ]
        return hists


class EpRatioEstimator(TransformerBase):

    def __init__(self, options, plot=False):
        super(EpRatioEstimator, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ('input', SingleHistInput(options.histname)),
            ('slicer', EpSlicer(options.pt, plot)),

        ])
