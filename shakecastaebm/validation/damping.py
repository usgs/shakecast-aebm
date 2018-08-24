import matplotlib.pyplot as plt

from shakecastaebm.damping import *
from shakecastaebm.demand import make_demand_spectrum
from shakecastaebm.spectrum import build_spectrum
from shakecastaebm.capacity import get_capacity
from shakecastaebm.data_tables import pref_periods
from .data import *

def run():
    capacity = get_capacity('PC1', 'high', 7, 24, 2, 1990, 'very_poor', 'poor')
    output = build_spectrum(hazard, pref_periods, insert=[capacity['elastic_period'], capacity['ultimate_period']], finish_val=0)
    demand = make_demand_spectrum(output)

    # damping
    kappa = get_kappa(capacity['performance_rating'], capacity['year'], mag, r_rup)
    b_eff = get_b_eff(capacity, kappa)

    beta = build_spectrum(b_eff, sanaz.t)
    dsf = get_dsf(beta, mag, r_rup)

    fig1 = plt.figure()
    plt.title('Beta Effective comparison')
    plt.plot([p['x'] for p in beta_check], [p['y'] for p in beta_check], 'o', label='Verification Curve')
    plt.plot([p['x'] for p in b_eff], [p['y'] for p in b_eff], 'o', label='Calculated Beta')
    plt.xlabel('Period (s)')
    plt.ylabel('Beta Effective')
    plt.legend()

    fig2 = plt.figure()
    plt.title('DSF Comparison')
    plt.plot([p['x'] for p in dsf_check], [p['y'] for p in dsf_check], label='Verification Curve')
    plt.plot([p['x'] for p in dsf], [p['y'] for p in dsf], label='Calculated DSF')
    plt.xlabel('Period (s)')
    plt.ylabel('DSF')
    plt.legend()

    return fig1, fig2

def main():
    fig1, fig2 = run()
    plt.show()

if __name__ == '__main__':
    main()

    
