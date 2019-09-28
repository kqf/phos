
PARTICLE_MASSES = {
    "#pi^{0}": 0.134976,
    "#eta": 0.547862,
}


def mass(particle):
    return PARTICLE_MASSES[particle]


def cross_section():
    return 57.8 * 1e3
