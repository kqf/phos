import spectrum.broot as br


class AnalysisReaderBase(object):
    def _events(self, filename, listname):
        return br.io.read(
            filename,
            listname,
            "EventCounter").GetBinContent(2)


# TODO: Fix this logic, convert to single input reader class
class SingleHistInput(AnalysisReaderBase):

    def __init__(self, histname, listname=None, norm=False):
        super(SingleHistInput, self).__init__()
        self.histname = histname
        self.listname = listname
        self.norm = norm

    def transform(self, data, loggs=None):
        # TODO: Fix this, histname should be always taken from the data

        hist = br.io.read(
            data.filename,
            self.listname or data.listname,
            self.histname
        )
        br.set_nevents(hist, self._events(
            data.filename,
            data.listname), self.norm)
        return hist


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
