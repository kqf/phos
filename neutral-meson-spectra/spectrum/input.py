import spectrum.broot as br


class AnalysisReaderBase(object):
    def _events(self, filename, listname):
        return br.io.read(
            filename,
            listname,
            "EventCounter").GetBinContent(2)


class Input(object):
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
        self.pt_range = tuple(pt_range)
        self.histnames = histnames or [
            "{}{}{}".format(self.prefix, p, self.histname)
            for p in self.suffixes]
        self.n_events = n_events
