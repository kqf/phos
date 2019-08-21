import ROOT

import array
import json
import re
import click
import six
import pandas as pd
from collections import defaultdict

PATTERNS = {
    "p_T": r"Pt +({float})",
    "#sigma_{total}": r"SIGTOT NLL +({float})",
    "#sigma_{born}": r"where  BORN = +({float})",
    "#sigma_{nlo}": r"HIGH ORDER = +({float})",
    "Kff": r"K factor  fragmentation  NLL/BORN    ({float})"
}

TITLES = {
    "#sigma_{total}":
    "#sigma_{total} NLO; E d^3 #sigma/dp^3 (mb GeV); p_T (GeV/c)",
    "#sigma_{born}":
    "#sigma_{born}; E d^3 #sigma/dp^3 (mb GeV); p_T (GeV/c)",
    "#sigma_{nlo}":
    "#sigma_{nlo}; E d^3 #sigma/dp^3 (mb GeV); p_T (GeV/c)",
    "Kff": "K-factob fragmentation; NLO/Born; p_T (GeV/c)",
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


def data2hists(data, edges):
    hist = ROOT.TH1F(data.name, TITLES[data.name], len(edges) - 1, edges)
    for i, v in enumerate(data.values):
        hist.SetBinContent(i, v)
    return hist


@click.command()
@click.option("--filename", type=click.Path(exists=True), required=True)
def main(filename):
    data = pd.DataFrame(parse_incnlo(filename)).sort_values("p_T")

    with open("../neutral-meson-spectra/config/data/pt.json") as f:
        edges = array.array('f', json.load(f)["#pi^{0}"]["ptedges"])

    for title in TITLES:
        data2hists(data[title], edges)


if __name__ == '__main__':
    main()
