import json
import hashlib
from spectrum.input import Input

class DataVault(object):
    def __init__(self):
        super(DataVault, self).__init__()
        with open('config/vault/ledger.json') as f:
            self._ledger = json.load(f)

    @classmethod
    def _validate_dataset(klass, filename, hsum_nominal):
        hashsum = hashlib.sha256()
        with open(filename) as f:
            data = f.read()
        hashsum.update(data)
        hsum_real = hashsum.hexdigest()

        msg = "File {0} doesn't match the desired hash {1} but got {2}".format(
            filename,
            hsum_nominal,
            hsum_real
        )

        if hsum_real != hsum_nominal:
            raise IOError(msg)


    def dataset(self, production, version="latest"):
        return self._ledger[production][version]


    def file(self, production, version="latest"):
        data = self.dataset(production, version)
        filename = data["file"]
        self._validate_dataset(filename, data["hsum"])
        return filename

    def input(self, production, version="latest", listname=None, histname='MassPt'):
        filename = self.file(production, version)
        if not listname:
            listname = self.dataset(production, version)['default_selection']
        return Input(filename, str(listname), histname)
