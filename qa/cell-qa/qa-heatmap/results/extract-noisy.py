#!/usr/bin/python

import ROOT

class XZExtractor(object):
    def __init__(self, filename, function, name):
        super(XZExtractor, self).__init__()
        self.modules = self.read(filename, function, name)
        self.cells = [[]]

    def noisy_cells(self, hists, thresholds):
        """
                The output of function can be used directly to remove noisy cells.
                There is no need to add + 1 to the coordinates
        """
        return [[[x + 1, z + 1, i + 1] for x in range(h.GetNbinsX()) for z in range(h.GetNbinsY()) if h.GetBinContent(x + 1, z + 1) > threshold] for i, (h, threshold) in enumerate(zip(hists, thresholds))]

    def inspect(self, thresholds):
        ROOT.gStyle.SetOptStat('')
        self.cells = self.noisy_cells(self.modules, thresholds)
        for i, (h, cells) in enumerate(zip(self.modules, self.cells)):
            for cell in cells: h.SetBinContent(cell[0], cell[1], 0)
            h.Draw('colz')
            canvas = ROOT.gROOT.FindObject('c1')
            canvas.Update()
            canvas.SaveAs('mod%d' %i + '.png')
            print ',\n'.join(map(str, cells)) + ',' ,' //',  len(cells),  'cells in the module %d' % i
            raw_input('')

        self.save('updated-hitmap.root', "HitMapCleaned%d", False)

    def read(self, filename, function, name):
        inlist = function(ROOT.TFile(filename))
        histograms = [inlist.FindObject(name % i) for i in range(1, 5)]
        return histograms

    def save(self, ofilename, oname, noisy_only = True):
        """
                By default this function saves only noisy cells.
                This can be canged usingoption noisy_only = False.
        """
        ofile = ROOT.TFile(ofilename, 'recreate')

        outhists = [h.Clone(oname % (i + 1)) for i, h in enumerate(self.modules)]
        for h, cells in zip(outhists, self.cells):
            if noisy_only: h.Reset()
            for cell in cells: h.SetBinContent(cell[0], cell[1], noisy_only * 1.)
            # h.Write()

        ofile.Write()
        ofile.Close()


class AbsIdExtractor(XZExtractor):
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
    infile = 'LHC16.root'

    print '// Low energy noise'
    extractor_low = XZExtractor(infile, lambda x: x.QualOnlyTender, 'hCluNXZM_0_SM%d')
    extractor_low.inspect([35000] * 4)

    print 
    print '// Now high energy noise'
    print 

    extractor_high = AbsIdExtractor(infile, lambda x: x.QualOnlyTender, 'hCluNXZM_1_SM%d')
    extractor_high.inspect([10000] * 4)

    # extractor.save('very-noisy-cells-LHC16k.root', 'PHOS_BadMap_mod%d')


if __name__ == '__main__':
    main()