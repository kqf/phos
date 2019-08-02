import hashlib
import json

from spectrum.input import Input, NoMixingInput


class DataVault(object):
    def __init__(self, ledger='ledger.json'):
        super(DataVault, self).__init__()
        with open('config/vault/' + ledger) as f:
            self._ledger = json.load(f)

    def _validate_dataset(self, production, version):
        dataset = self.dataset(production, version)

        hsum_nominal = dataset["hsum"]
        filename = dataset["file"]

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
        self._validate_dataset(production, version)
        return self.dataset(production, version)["file"]

    def input(self, production, version="latest",
              listname=None, pt_range=None, use_mixing=True,
              *args, **kwargs):

        filename = self.file(production, version)
        if not listname:
            listname = self.dataset(production, version)['default_selection']

        if not pt_range:
            pt_range = self.dataset(production, version)['pt_range']

        transformer = Input if use_mixing else NoMixingInput
        return transformer(filename, str(listname), pt_range=pt_range,
                           *args, **kwargs)

    def modules_input(self, production, version="latest", listname="Phys",
                      same_module=True, *args, **kwargs):
        inputs = Input.read_per_module(
            self.file(production, version),
            listname,
            same_module=same_module
        )
        return inputs
