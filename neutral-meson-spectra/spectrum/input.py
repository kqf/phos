import spectrum.broot as br


class AnalysisReaderBase(object):
    def _events(self, filename, listname):
        return br.io.read(
            filename,
            listname,
            "EventCounter").GetBinContent(2)
