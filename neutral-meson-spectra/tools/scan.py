from spectrum.analysis import Analysis
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline, ParallelPipeline, HistogramSelector
from spectrum.broot import BROOT as br


# class NonlinearityExtractor(TransformerBase):
#     def transform(self, data, loggs):
#         output = []
#         for d in data:
#             real, mixing = d.transform()
#             try:
#                 output.append(
#                     map(float, real.GetTitle().split())
#                 )
#             except ValueError:
#                 output.append(None)
#         return output


class NonlinearityScan(TransformerBase):
    def __init__(self, options, plot=False):
        super(NonlinearityScan, self).__init__()
        mass_estimator = Pipeline([
            ("reconstruction", Analysis(options.analysis, plot)),
            ("mass", HistogramSelector("mass")),
        ])

        mass_estimator_data = Pipeline([
            ("reconstruction", Analysis(options.analysis_data, plot)),
            ("mass", HistogramSelector("mass")),
        ])

        self.pipeline = ParallelPipeline([
            ("mass_data", mass_estimator_data)] + [
            ("mass" + str(i), mass_estimator)
            for i in range(options.nbins ** 2)
        ])

    def transform(self, data, loggs):
        # titles = NonlinearityExtractor().transform(data, loggs)
        # print titles
        out = self.pipeline.transform(data, loggs)
        data = out[0]
        mc = out[1:]
        return [br.chi2ndf(hist, data) for hist in mc]
