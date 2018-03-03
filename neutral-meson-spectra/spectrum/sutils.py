import ROOT
from math import sqrt
from collections import Iterable
import array
import os

def prepare_directory(name):
    path = "/".join(
        name.split('/')[0:-1] # remove filename
    )

    if not os.path.isdir(path):
        os.makedirs(path, 0755)
    return name


def wait(name='', draw=True, save=False, suffix=''):
    if save and not draw:
        ROOT.gROOT.SetBatch(True)
        
    outdir = 'results/'
    canvas = gcanvas()
    canvas.Update()
    name = (name
        .replace(' ', '-')
        .replace('_', '-')
        .replace(',', '-')
        .replace('(', '')
        .replace(')', '')
    )
    if save:
        canvas.SaveAs(prepare_directory(outdir + name + '.pdf'))

    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: 
        ROOT.gApplication.Run(True)

def canvas(name, x=1., y=1., scale=6):
    canvas = ROOT.TCanvas('c1', 'Canvas', int(128 * x * scale) , int(96 * y * scale))
    ticks(canvas)
    return adjust_canvas(canvas)

def gcanvas(x = 1., y = 1, resize = False, scale = 6):
    ccanvas = ROOT.gROOT.FindObject('c1')
    if ccanvas: 
        if not resize:
            ccanvas.cd()
            return ccanvas 

        cx, cy = map(int, [128 * x * scale, 96 * y * scale])
        ccanvas.SetWindowSize(cx, cy)
        ccanvas.SetCanvasSize(cx, cy)
        return adjust_canvas(ccanvas)
    return canvas("c1", x, y, scale)




def adjust_labels(hist1, hist2, scale = 1):
    if not hist1 or not hist2:
        return None

    hist1.SetTitleOffset(hist2.GetTitleOffset('X')        , 'X')
    hist1.SetTitleOffset(hist2.GetTitleOffset('Y') / scale, 'Y')
    hist1.SetTitleSize(hist2.GetTitleSize('X') * scale, 'X')
    hist1.SetTitleSize(hist2.GetTitleSize('Y') * scale, 'Y')
    hist1.SetLabelSize(hist2.GetLabelSize('X') * scale, 'X')
    hist1.SetLabelSize(hist2.GetLabelSize('Y') * scale, 'Y')
    return hist1


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
       
def adjust_canvas(canvas):
    height = canvas.GetWindowHeight()
    canvas.SetBottomMargin(0.02 * height)
    canvas.SetTopMargin(0.02 * height)

    width = canvas.GetWindowWidth()
    canvas.SetRightMargin(0.01 * width)
    canvas.SetLeftMargin(0.01 * width)
    return canvas
    
    
def tsallis(x, p, a = 0.135, b = 0.135, bias = 0):
    return (x[0] + x[0] * bias)*p[0]/2./3.1415*(p[2]-1.)*(p[2]-2.)/(p[2]*p[1]*(p[2]*p[1]+b*(p[2]-2.))) * (1.+(sqrt((x[0] +x[0] * bias)*(x[0] +x[0] * bias)+a*a)-b)/(p[2]*p[1])) ** (-p[2])


def equals(a, b, tol = 1e-7):
    if isinstance(a,Iterable):
        return all(map(lambda x, y: equals(x, y, tol), zip(a, b)))
    return abs(a - b) < tol 

    
def in_range(x, somerange):
    a, b = somerange
    return a < x < b


    
class Cc:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def fail(s): 
        return '{0}{1}{2}'.format(Cc.FAIL, s, Cc.ENDC)

    @staticmethod
    def warning(s): 
        return '{0}{1}{2}'.format(Cc.warning, s, Cc.ENDC)

    @staticmethod
    def ok(s): 
        return '{0}{1}{2}'.format(Cc.OKGREEN, s, Cc.ENDC)
 