
PARTICLE_MASSES = {
    "#pi^{0}": 0.134976,
    "#eta": 0.547862,
}

PAVE_PREFIX = """
pp at #sqrt{#it{s}} = 13 TeV
"""

PDG_BR_RATIO = {
    "#pi^{0}": 0.9882,
    "#eta": 0.3931,
}


def mass(particle):
    return PARTICLE_MASSES[particle]


def cross_section():
    return 57.8 * 1e3


def invariant_cross_section_code(scale="mb"):
    output = (
        "#it{{E}} "
        "#frac{{ d^{{3}}#sigma }}{{ d#it{{p}}^{{3}} }} "
        "({} GeV^{{-2}} #it{{c^{{3}}}})"
    ).format(scale).strip().replace("\n", "")
    return output
