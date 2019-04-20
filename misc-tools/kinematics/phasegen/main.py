import ROOT
from phasegen.analysis import Analysis
from math import pi


class AngleSelection(object):
    def __init__(self, ofile="output.root"):
        super(AngleSelection, self).__init__()
        self.ofile = ofile
        title = "Opening angle between two photons; #theta, rad"
        self.angle = ROOT.TH1F("hAngle", title, 10000, 0, pi / 2)
        title = "Opening angle between two photons vs momentum"
        title += "; #theta, rad; p, GeV/c"
        self.angle_p = ROOT.TH2F(
            "hAngleMomentum", title, 5000, 0, pi / 2, 1000, 15, 100)
        title = "Initial #pi^{0} meson momentum (tsallis); p, GeV/c"
        self.original = ROOT.TH1F("hP", title, 1000, 15, 100)

    def transform(self, particles):
        (first, second), original = particles
        angle = first.Angle(second.Vect())
        self.angle.Fill(angle)
        self.angle_p.Fill(angle, original.P())
        self.original.Fill(original.P())

    def write(self):
        ofile = ROOT.TFile(self.ofile, "recreate")
        self.angle.Write()
        self.angle_p.Write()
        self.original.Write()
        ofile.Close()


def main():
    angle_distribution = AngleSelection()
    Analysis().transform(
        [angle_distribution]
    )
    angle_distribution.write()


if __name__ == '__main__':
    main()
