# Convert cell (X, Z) to absID without geometry.
# Be careful in case if gemetry changes.

import ROOT
import json
import click


def inspect_modules(hists):
    return [[[x, z, i + 1]
             for x in range(h.GetNbinsX())
             for z in range(h.GetNbinsY())
             if h.GetBinContent(x + 1, z + 1) > 0]
            for i, h in enumerate(hists)]


class Converter(object):
    sizex, sizez = 64, 56
    size = sizex * sizez
    feex, feez = 16, 2
    cellmsg = '\nCell numbering ranges from: (0,0) to (63, 55)'
    feemsg = '\nFEE numbering ranges from: (0,0) to (3, 27)'

    def __init__(self, input_file):
        super(Converter, self).__init__()
        if '.root' in input_file:
            self.cells, self.fees = self.from_root(input_file)
        else:
            self.cells, self.fees = self.read(input_file)
        assert self.cells or self.fees, "Nothing to convert!"

    def from_root(self, input_file):
        infile = ROOT.TFile.Open(input_file, 'r')
        hists = [infile.Get('PHOS_BadMap_mod%d;1' % i) for i in range(1, 5)]
        cells = inspect_modules(hists)
        return sum(cells, []), []

    def read(self, input_file):
        with open(input_file, 'r') as f:
            data = json.load(f)
        return data['cells'], data['fees']

    def convert(self):
        cells, fees = [], []
        if self.cells:
            cells = map(self.convert_cell, *zip(*self.cells))

        if self.fees:
            fees = map(self.convert_fee, *zip(*self.fees))

        all_cells = sum(fees, cells)

        print ','.join(map(str, all_cells))
        print len(all_cells), '      length of the sequence'

    def convert_cell(self, x, z, sm):
        # In this convention (0, 0, 1) is a first cell of module 1.
        message = "{xz} cooridnate of cell is wrong {xz} = {val} !!!{msg}"
        assert x < self.sizex, message.format(xz="X", val=x, msg=self.cellmsg)
        assert x < self.sizex, message.format(xz="Z", val=z, msg=self.cellmsg)
        return (sm - 1) * self.size + x * self.sizez + z + 1

    def convert_fee(self, x, z, sm):
        message = "{xz} cooridnate of FEE is wrong {xz} = {val} !!!{msg}"

        xmessage = message.format(xz="X", val=x, msg=self.cellmsg)
        assert x < self.sizex / self.feex, xmessage

        zmessage = message.format(xz="Z", val=z, msg=self.cellmsg)
        assert z < self.sizez / self.feez, zmessage

        x, z = self.feex * x, self.feez * z
        # Convert fee coordinate to a set of 32 cell coordinates
        cells = [(i, j, sm)
                 for i in range(x, x + self.feex)
                 for j in range(z, z + self.feez)
                 ]
        return map(self.convert_cell, *zip(*cells))


@click.command()
@click.option('--filename', required=True)
def main(filename):
    Converter(filename).convert()
