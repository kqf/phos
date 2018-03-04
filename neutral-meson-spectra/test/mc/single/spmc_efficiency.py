import unittest
import ROOT

from spectrum.input import Input
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.options import EfficiencyOptions, MultirangeEfficiencyOptions


def evaluate_spmc_efficiency(unified_inputs, particle):
    
    estimator = EfficiencyMultirange(
       MultirangeEfficiencyOptions.spmc(unified_inputs, particle) 
    )

    loggs = AnalysisOutput("multirange_efficiency_spmc_{}".format(particle), particle)

    efficiency = estimator.transform(
       [Input(filename, "PhysEff") for filename in unified_inputs],
       loggs
    )

    efficiency.SetTitle(
        "#varepsilon = #Delta #phi #Delta y/ 2 #pi " \
        "#frac{Number of reconstructed %s}{Number of generated primary %s}" \
            % (particle, particle)
    )
    diff = Comparator()
    diff.compare(efficiency)
    loggs.plot(False)
    

