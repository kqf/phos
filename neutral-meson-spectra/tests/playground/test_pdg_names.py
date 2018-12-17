import ROOT
import pytest
import re

PDG_PARTICLES = [
    1, 2, 3, 4, -313, -213,
    221, 323, 21, 310, 313, 223, -323, 213
]

KNOWN_PARTICLES = {
    "Xi", "Sigma", "Lambda", "Delta",
    "rho", "omega", "eta", "phi", "pi"
}


def pdg2name(x):
    return ROOT.TParticle(x, *[0] * 13).GetName()

# @unittest.skip("")


@pytest.mark.parametrize("pdg", PDG_PARTICLES)
def test_converts_names(pdg):
    pname = pdg2name(pdg)
    print pdg, pname, name2rootname(pname)


def name2rootname(name):
    for s in re.findall(r"[^a-zA-Z_]", name):
        name = name.replace(s, "^{" + s + "}")

    if "_bar" in name:
        name = name.replace("_bar", "")
        name = "#bar" + name

    for k in KNOWN_PARTICLES:
        if k in name:
            name = name.replace(k, "#" + k)

    if "_" in name:
        idx = name.find("_")
        name = name.replace(name[idx:], "_{" + name[idx + 1:] + "}")

    return name
