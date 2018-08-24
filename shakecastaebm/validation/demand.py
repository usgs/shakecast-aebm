import matplotlib.pyplot as plt

from shakecastaebm.damping import damp
from shakecastaebm.demand import make_demand_spectrum
from shakecastaebm.spectrum import build_spectrum
from shakecastaebm.capacity import get_capacity
from shakecastaebm.data_tables import pref_periods
from .data import *

import copy

def run():
    capacity = get_capacity('PC1', 'high', 7, 24, 2, 1990, 'very_poor', 'poor')
    output = build_spectrum(hazard, pref_periods, insert=[capacity['elastic_period'], capacity['ultimate_period']], finish_val=0)
    demand = make_demand_spectrum(output)

    damped_demand = damp(demand, capacity, mag, r_rup)

    fig1 = plt.figure()
    plt.title('Input Hazard')
    plt.plot([p['x'] for p in hazard], [p['y'] for p in hazard], 'o', label='Input Hazard')
    plt.plot([p['x'] for p in output], [p['y'] for p in output], label='Expanded Hazard')
    plt.xlabel('Period (s)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.legend()

    fig2 = plt.figure()
    plt.title('Demand Curve')
    plt.plot([p['disp'] for p in demand], [p['y'] for p in demand], label='Raw Demand')
    plt.plot([p['disp'] for p in damped_demand], [p['y'] for p in damped_demand], label='Damped Demand')
    plt.xlabel('Spectral Displacement (inches)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.legend()

    return fig1, fig2

def main():
    fig1, fig2 = run()
    plt.show()

if __name__ == '__main__':
    main()
