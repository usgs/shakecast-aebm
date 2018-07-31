import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from ..damping import *
from ..demand import make_demand_spectrum
from ..spectrum import build_spectrum
from ..capacity import get_capacity
from ..data_tables import pref_periods
from data import *

def run():
    capacity = get_capacity('PC1', 'high', 7, 24, 2, 1990, 'very_poor', 'poor')
    output = build_spectrum(hazard, pref_periods, insert=[capacity['elastic_period'], capacity['ultimate_period']], finish_val=0)
    demand = make_demand_spectrum(output)

    # damping
    kappa = get_kappa(capacity['performance_rating'], capacity['year'], mag, r_rup)
    b_eff = get_b_eff(capacity, kappa)

    beta = build_spectrum(b_eff, sanaz.t);
    dsf = get_dsf(beta, mag, r_rup)

    fig = plt.figure()
    plt.plot([p['x'] for p in dsf_check], [p['y'] for p in dsf_check], label='Validation Curve')
    plt.plot([p['x'] for p in dsf], [p['y'] for p in dsf], label='Calculated Curve')
    plt.legend()

    return fig

def main():
    fig = run()
    plt.show()

if __name__ == '__main__':
    main()

    
