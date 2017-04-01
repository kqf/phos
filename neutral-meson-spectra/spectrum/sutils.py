import ROOT
from math import sqrt
from collections import Iterable

def tsallis(x, p, a = 0.135, b = 0.135):
    return x[0]*p[0]/2./3.1415*(p[2]-1.)*(p[2]-2.)/(p[2]*p[1]*(p[2]*p[1]+b*(p[2]-2.))) * (1.+(sqrt(x[0]*x[0]+a*a)-b)/(p[2]*p[1])) ** (-p[2])

def area_and_error(hist, a, b):
    area, areae = ROOT.Double(), ROOT.Double()
    bin = lambda x: hist.FindBin(x)
    area = hist.IntegralAndError(bin(a), bin(b), areae)
    return area, areae

    
def ratio(hist1, hist2, title, label = ''):
    ratio = hist1.Clone(hist1.GetName() + '_ratio')
    ratio.SetTitle(title)
    ratio.label = label

    ratio.Divide(hist1, hist2, 1, 1, "B")
    return ratio


def equals(a, b, tol = 1e-7):
    if isinstance(a,Iterable):
        return all(map(lambda x, y: equals(x, y, tol), zip(a, b)))
    return abs(a - b) < tol 

def wait(name, draw=True, save = False, suffix = ''):
    canvas = get_canvas()
    canvas.Update()
    name = name.replace(' ', '_')
    if save: canvas.SaveAs('results/' + name + '.pdf')

    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)


def draw_and_save(histograms, name = '', draw = True, save = True, suffix = ''):
    ROOT.gStyle.SetOptStat('erm')
    histograms = [h.Clone(h.GetName() + str(id(h))) for h in histograms]
    if name: 
        for h in histograms: h.SetTitle(name.replace('_', ' ') + ' ' + suffix + ' ' + h.GetTitle())

    histograms[0].Draw()
    for h in histograms: h.Draw('same')
    wait(name + histograms[0].GetName() +  '_' + suffix , draw, save)

def ticks(pad):
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy() 
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky() 
    pad.SetTickx()
    pad.SetTicky() 
    pad.SetGridx()
    pad.SetGridy()
    return pad
       
def nicely_draw(hist, option = '', legend = None):
    hist.Draw(option)

    if 'spectrum' in hist.GetName(): 
        ROOT.gPad.SetLogy()
    else:
        ROOT.gPad.SetLogy(0)

    legend = legend if legend else ROOT.TLegend(0.9, 0.4, 1.0, 0.6)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.AddEntry(hist, hist.label)
    legend.Draw('same')
    wait('xlin_' + hist.GetName(), draw = True, save = True)

def get_canvas(x = 1., y = 1, resize = False):
    canvas = ROOT.gROOT.FindObject('c1')
    if canvas: 
        if resize: canvas.Clear()
        ticks(canvas)
        return canvas 

    canvas = ROOT.TCanvas('c1', 'Canvas', int(128 * x * 6) , int(96 * y * 6))
    ticks(canvas)
    return canvas



def adjust_canvas(canvas):
    height = canvas.GetWindowHeight()
    canvas.SetBottomMargin(0.02 * height)
    canvas.SetTopMargin(0.02 * height)

    width = canvas.GetWindowWidth()
    canvas.SetRightMargin(0.01 * width)
    canvas.SetLeftMargin(0.01 * width)
    return canvas


class Cc:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def fail(s): 
        return Cc.FAIL + s + Cc.ENDC

    @staticmethod
    def warning(s): 
        return Cc.WARNING + s + Cc.ENDC

    @staticmethod
    def ok(s): 
        return Cc.OKGREEN + s + Cc.ENDC 
 