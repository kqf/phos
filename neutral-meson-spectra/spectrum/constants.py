
PARTICLE_MASSES = {
    "#pi^{0}": 0.134976,
    "#eta": 0.547862,
}

PAVE_PREFIX = """
pp at #sqrt{s} = 13 TeV
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
    return """
    E #frac{{ d^{{3}}#sigma }}{{ dp^{{3}} }} ({} GeV^{{-2}} #it{{c^{{3}}}})
    """.format(scale)
