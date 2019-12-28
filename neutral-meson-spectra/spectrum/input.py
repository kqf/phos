import spectrum.broot as br

# TODO: Fix this logic, remove Input class


class AnalysisInputBase(object):
    def _events(self, filename, listname):
        return br.io.read(
            filename,
            listname,
            "EventCounter").GetBinContent(2)


class SingleHistInput(AnalysisInputBase):

    def __init__(self, histname, listname=None, priority=999, norm=False):
        super(SingleHistInput, self).__init__()
        self.histname = histname
        self.listname = listname
        self.priority = priority
        self.norm = norm

    def transform(self, inputs, loggs=None):
        hist = br.io.read(
            inputs.filename,
            self.listname or inputs.listname,
            self.histname
        )
        br.set_nevents(hist, self._events(
            inputs.filename,
            inputs.listname), self.norm)
        hist.priority = self.priority
        return hist


class Input(AnalysisInputBase):
    def __init__(
        self,
        filename,
        listname,
        histname="MassPt",
        pt_range=(0., 20.),
        suffixes=("", "Mix"),
        histnames=None,
        n_events=None,
        prefix="h",
    ):
        super(Input, self).__init__()
        self.filename = filename
        self.listname = listname
        self.histname = histname
        self.suffixes = suffixes or ("", )
        self.prefix = prefix
        self.pt_range = pt_range
        self.histnames = histnames or [
            "{}{}{}".format(self.prefix, p, self.histname)
            for p in self.suffixes]

    def transform(self, data=None, outputs=None):
        hists = br.io.read_multiple(
            self.filename,
            self.listname,
            self.histnames
        )
        for h in hists:
            br.set_nevents(h, self._events(self.filename, self.listname))
        return hists
