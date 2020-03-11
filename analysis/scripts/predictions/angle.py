import pytest
import ROOT
import array
import tqdm

import spectrum.constants as ct
import spectrum.plotter as plt
from math import pi
from spectrum.vault import FVault


def mometum(pt, mass=0, eta=0, phi=5.1):
    p = ROOT.TLorentzVector()
    p.SetPtEtaPhiM(pt, eta, phi, mass)
    return p


class GeneratedPlots:
    def __init__(self, phi_cut=2, y_cut=0.13):
        self.phi_cut = phi_cut
        self.y_cut = y_cut
        self.etaphi = ROOT.TH2F(
            "etaphi", ";#phi (rad); #it{y}",
            100, 0, 2 * pi,
            100, -1, 1)
        self.phi = ROOT.TH1F(
            "etaphi", ";#Delta #phi (rad); counts",
            100, 0, 2 * pi)
        self.rawphi = ROOT.TH1F(
            "retaphi", ";#Delta #phi (rad); counts",
            100, 0, 2 * pi)

    def update(self, p1, p2):
        p = p1 - p2
        self.rawphi.Fill(p.Phi())
        if abs(p.Phi()) > self.phi_cut or abs(p.Eta()) > self.y_cut:
            return
        self.etaphi.Fill(p.Phi(), p.Eta())
        self.phi.Fill(p.Phi())


class DecayGenerator():
    def __init__(self, particle, nevents=100000, nphot=2):
        self.particle = particle
        self.nevents = nevents
        self.nphot = nphot
        self.masses = array.array('d', [0, 0])
        self.mass = ct.mass(particle)
        self.pt = FVault().tf1("tcm", "{} 13 TeV".format(particle))

    def decay(self):
        event = ROOT.TGenPhaseSpace()
        pdecay = mometum(self.pt.GetRandom(), self.mass)
        event.SetDecay(pdecay, self.nphot, self.masses)
        event.Generate()
        return [event.GetDecay(i) for i in range(self.nphot)]

    def transform(self, selections):
        for e in tqdm.trange(self.nevents):
            p1, p2 = self.decay()
            selections.update(p1, p2)


@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"]
)
def test_distributions(particle, stop):
    generator = DecayGenerator(particle)
    plots = GeneratedPlots()
    generator.transform(plots)
    with plt.canvas(stop=stop):
        plots.etaphi.Draw("colz")

    plt.hplot([plots.phi, plots.rawphi], logy=False, logx=False)
