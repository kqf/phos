import sys
import ROOT

def badmap(hists, canvas=None, scale=5):
    if not canvas:
        canvas = ROOT.TCanvas("c1", "canvas", 128 * scale, 96 * scale)
        canvas.Divide(2, 2)

    for i, sm in enumerate(hists):
        canvas.cd(i + 1)
        # print sm.label, sm.GetEntries()
        sm.Draw(sm.option)
    canvas.Update()

    try:
        canvas.SaveAs(hists[0].oname)
    except AttributeError:
        canvas.SaveAs("{}.pdf".format(hists[0].GetName()))


@click.command()
@click.option('--file', '-c',
              type=click.Path(exists=True),
              help='Path to the .root file',
              required=True)
def main(file):
    infile = ROOT.TFile(file)
    hists = [k.ReadObj() for k in infile.GetListOfKeys()]
    badmap(hists)
