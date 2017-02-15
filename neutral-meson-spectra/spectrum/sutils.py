import ROOT


def wait(name, draw, save = True, suffix = ''):
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
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky() 
    for h in histograms: h.Draw('same')
    wait(name + histograms[0].GetName() +  '_' + suffix , draw, save)

       
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

def get_canvas(x = 1, y = 1, resize = False):
    canvas = ROOT.gROOT.FindObject('c1')
    if canvas: 
        # if resize: canvas.SetWindowSize(int(128 * x * 6) , int(96 * y * 6))
        return canvas 

    return ROOT.TCanvas('c1', 'Canvas', int(128 * x * 6) , int(96 * y * 6))

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
 