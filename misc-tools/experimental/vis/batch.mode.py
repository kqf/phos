import ROOT
from contextlib import contextmanager


@contextmanager
def rfile(filename, mode="recreate"):
    fileio = ROOT.TFile(filename, mode)
    yield fileio
    fileio.Close()


def ccanvas(name, x=1., y=1., scale=6):
    canvas = ROOT.TCanvas('c1', 'Canvas', int(
        128 * x * scale), int(96 * y * scale))
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    canvas.SetTickx()
    canvas.SetTicky()
    canvas.SetGridx()
    canvas.SetGridy()
    return canvas


def gcanvas(x=1., y=1, resize=False, scale=8):
    canvas = ROOT.gROOT.FindObject('c1')
    if canvas:
        if not resize:
            canvas.cd()
            return canvas

        cx, cy = map(int, [128 * x * scale, 96 * y * scale])
        canvas.SetWindowSize(cx, cy)
        canvas.SetCanvasSize(cx, cy)
    return ccanvas("c1", x, y, scale)


def main():
    for i in range(100):
        canvas = gcanvas()
        output = ROOT.TH1F("hist_{}".format(i), "thist", 20, 0, 20)
        output.FillRandom("gaus")
        output.Draw()
        canvas.Update()
        canvas.Connect("Closed()", "TApplication",
                       ROOT.gApplication, "Terminate()")
        canvas.Show()
        with rfile("test.root", "update"):
            canvas.Write("canvas{}".format(i))


if __name__ == '__main__':
    main()
