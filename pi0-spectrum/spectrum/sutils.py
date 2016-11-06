import ROOT


def draw_and_save(name, draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs('results/' + name + '.pdf')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)
    
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
    draw_and_save('xlin_' + hist.GetName(), save = True)
  