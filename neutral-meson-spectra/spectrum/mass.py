class BackgroundEstimator(object):

    def transform(self, mass):
        if not mass.mass.GetEntries():
            return mass.mass

        sigf, bgrf = mass.peak_function.fit(mass.mass)
        bgrf.SetLineColor(8)
        bgrf.SetFillColor(8)
        bgrf.SetFillStyle(3436)
        mass.background = bgrf
        return mass

class SignalExtractor(object):

    def transform(self, mass):
        if not mass.mass.GetEntries():
            return mass.mass

        signal = mass.mass.Clone()
        signal.Add(mass.background, -1)

        mass.signal = signal
        return mass


class SignalFitter(object):

    def transform(self, mass):
        mass.sigf, mass.bgrf = mass.peak_function.fit(mass.signal)
        return mass


    
class MassFitter(object):

    def __init__(self, options, label):
        super(MassFitter, self).__init__()
        self.opt = options

    def transform(self, masses):

        pipeline = [
            BackgroundEstimator(),
            SignalExtractor(),
            SignalFitter()
        ]

        for mass in masses:
            for estimator in pipeline:
                estimator.transform(mass)

        return masses
  