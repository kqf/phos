from spectrum.efficiency import EfficiencyMultirange
from spectrum.comparator import Comparator
from vault.datavault import DataVault



class FitEfficiency(object):


    def __init__(self, particle, fitf):
        self.particle = particle
        self.fitfunction = fitf


    def fit_efficiency(self, efficiency):
        if not self.fitfunction:
            return efficiency

        efficiency.Fit(self.fitfunction, "R")
        Comparator().compare(efficiency)
        return efficiency


    def efficiency(self, fileranges):
        efficiency_estimator = EfficiencyMultirange(
            'hPt_{0}_primary_'.format(self.particle),
            'eff',
            {
                DataVault().file("single #pi^{0}", "low"): (0, 7),
                DataVault().file("single #pi^{0}", "high"): (7, 20)
            }
        )

        efficiency = efficiency_estimator.eff()
        efficiency.SetTitle(
            '#varepsilon = #Delta #phi #Delta y/ 2 #pi ' \
            '#frac{Number of reconstructed %s}{Number of generated primary %s}' \
                % (self.particle, self.particle) 
        )
        diff = Comparator()
        return diff.compare(efficiency)

    def estimate(self, fileranges):
        pipeline = [
            self.efficiency,
            self.fit_efficiency
        ]

        data = fileranges
        for op in pipeline:
            data = op(data)

        return data
        

  