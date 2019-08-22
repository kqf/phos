import ROOT

import array
import json
import re
import click
import six
import pandas as pd
from collections import defaultdict
ROOT.TH1.AddDirectory(False)

PATTERNS = {
    "p_T": r"Pt +({float})",
    "#sigma_{total}": r"SIGTOT NLL +({float})",
    "#sigma_{born}": r"where  BORN = +({float})",
    "#sigma_{nlo}": r"HIGH ORDER = +({float})",
    "Kff": r"K factor  fragmentation  NLL/BORN    ({float})"
}

TITLES = {
    "#sigma_{total}":
    "#sigma_{total}; p_{T} (GeV/c); E d^{3} #sigma/dp^{3} (mb GeV)",
    "#sigma_{born}":
    "#sigma_{born}; p_{T} (GeV/c); E d^{3} #sigma/dp^{3} (mb GeV)",
    "#sigma_{nlo}":
    "#sigma_{nlo}; p_{T} (GeV/c); E d^{3} #sigma/dp^{3} (mb GeV)",
    "Kff": "K-factor fragmentation; p_{T} (GeV/c); NLO/Born",
}
FLOAT = r"[+-]?([0-9]*[.])?[0-9]+"


def parse_incnlo(filename):
    data = defaultdict(list)
    for line in open(filename):
        for title, pattern in six.iteritems(PATTERNS):
            match = re.search(pattern.format(float=FLOAT), line)
            if match:
                data[title].append(float(match.group(1)))
    return data


def data2hists(data, edges, scale=1e9):
    hist = ROOT.TH1F(data.name, TITLES[data.name], len(edges) - 1, edges)
    for i, v in enumerate(data.values):
        # Convert cross sections to mb
        hist.SetBinContent(i + 1, v / scale)
    return hist


@click.command()
@click.option("--filename", type=click.Path(exists=True), required=True)
@click.option("--ofilename", type=click.Path(exists=False), required=True)
def main(filename, ofilename):
    data = pd.DataFrame(parse_incnlo(filename)).sort_values("p_T")

    with open("../neutral-meson-spectra/config/data/pt.json") as f:
        edges = array.array('f', json.load(f)["#pi^{0}"]["ptedges"])

    hists = [data2hists(data[title], edges) for title in TITLES]
    print(hists)

    output = ROOT.TList()
    # output.SetOwner(True)
    for hist in hists:
        output.Add(hist)

    ofile = ROOT.TFile(ofilename, "recreate")
    output.Write("pQCD", 1)
    ofile.Write()
    ofile.Close()


if __name__ == '__main__':
    main()
