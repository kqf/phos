#!/usr/bin/python

import ROOT

class ExctractNoisy(object):
    def __init__(self, filename, function, name):
        super(ExctractNoisy, self).__init__()
        self.modules = self.read(filename, function, name)
        self.cells = [[]]

    def noisy_cells(self, hists, threshold):
        return [[[x, z, i + 1] for x in range(h.GetNbinsX()) for z in range(h.GetNbinsY()) if h.GetBinContent(x + 1, z + 1) > threshold] for i, h in enumerate(hists)]

    def inspect(self, threshold = 2000):
        self.cells = self.noisy_cells(self.modules, threshold)
        for h, cells in zip(self.modules, self.cells):
            for cell in cells: h.SetBinContent(cell[0] + 1, cell[1] + 1, 0)
            # h.Draw('lego')
            # ROOT.gROOT.FindObject('c1').Update()
            # raw_input('')

    def read(self, filename, function, name):
        inlist = function(ROOT.TFile(filename))
        histograms = [inlist.FindObject(name % i) for i in range(1, 5)]
        return histograms

    def save(self, ofilename, oname):
        ofile = ROOT.TFile(ofilename, 'recreate')

        outhists = [h.Clone(oname % (i + 1)) for i, h in enumerate(self.modules)]
        for h, cells in zip(outhists, self.cells):
            h.Reset()
            for cell in cells: h.SetBinContent(cell[0] + 1, cell[1] + 1, 1)
            # h.Write()

        ofile.Write()
        ofile.Close()


class AbsIdExtractor(ExctractNoisy):
    def __init__(self, filename, function, name, tolerance = 3):
        super(AbsIdExtractor, self).__init__(filename, function, name)
        # Number of cells that are neighboring
        self.tol = tolerance

    def noisy_cells(self, hists, thresholds):
        return [{ int(h.GetBinCenter(i + 1)): h.GetBinContent(i + 1) for i in range(h.GetNbinsX()) if h.GetBinContent(i + 1) > t} for h, t in zip(hists, thresholds)]


    def inspect(self, thresholds):
        self.cells = self.local_noise(self.noisy_cells(self.modules, thresholds))
        for i, cells in enumerate(self.cells):
            if not cells: continue
            print ','.join(map(str, cells)) + ',' ,' //',  len(cells),  'cells in module', i + 1
            # print ','.join(map(str, values)) + ',' ,' //',  len(cells),  'cells in module', i + 1

    def local_noise(self, cells):
        import operator
        # Find key (Id) with maximal value (entries)
        max_key = lambda inp:  max(inp.iteritems(), key=operator.itemgetter(1))[0]
        # Find all neighbour cells
        close_cells = lambda inp: [{c: inp[c] for c in inp if are_close(k, c, self.tol)} for k in inp]
        # Convert list of keys to a sub dictionary of original dictionary orig
        sublist = lambda keys, orig: {k: orig[k] for k in keys}

        maximal = [sublist(set(max_key(s) for s in close_cells(sm)), sm) for sm in cells]
        return maximal

def are_close(a, b, tol):
    cell_x = lambda c: c / 56 + 1
    cell_z = lambda c: c % 56
    return abs(cell_x(a) - cell_x(b)) <= tol or abs(cell_z(a) - cell_z(b)) <= tol



def main():
    infile = 'LHC16o.root'

    print '// Low energy noise'
    extractor_low = AbsIdExtractor(infile, lambda x: x.PhysTender, 'hClusterIdN_0_SM%d', tolerance = 2)
    extractor_low.inspect([3750, 6530, 8300, 8000])

    print 
    print '// Now high energy noise'
    print 

    extractor_high = AbsIdExtractor(infile, lambda x: x.PhysTender, 'hClusterIdN_1_SM%d', tolerance = 0)
    extractor_high.inspect([7000, 2500, 6300, 6000])

    # extractor.save('very-noisy-cells-LHC16k.root', 'PHOS_BadMap_mod%d')


if __name__ == '__main__':
    main()