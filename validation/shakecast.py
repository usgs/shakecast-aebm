import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from ..performance_point import performance_point
from ..demand import get_demand
from ..spectrum import build_spectrum
from ..damage import *
from ..capacity import *
from ..aebm import run as run_aebm
from ..data_tables import pref_periods
from data import *

def run():
    # run shakecast example
    hazard = [
        {'x': .03, 'y': 1.1377},
        {'x': 1.0, 'y': .8302},
        {'x': 3.0, 'y': .348}
    ]

    hazard_beta = .5
    mag = 6.7
    r_rup = 20

    capacity = get_capacity('C2', 'high', 1, 24, 2, 1990, 'very_poor', 'poor')
    damage_probs, capacity, demand, lower_demand, upper_demand, med_intersections, lower_intersections, upper_intersections = run_aebm(capacity, hazard, hazard_beta, pref_periods, mag, r_rup)

    pp_fig = plt.figure()
    plt.plot([p['disp'] for p in demand],
        [p['y'] for p in demand], '-ro', label='Median Demand')
    plt.plot([p['disp'] for p in upper_demand],
        [p['y'] for p in upper_demand], label='Upper bound demand')
    plt.plot([p['disp'] for p in lower_demand],
        [p['y'] for p in lower_demand], label='Lower bound demand')
    plt.plot([p['x'] for p in capacity['curve']],
        [p['y'] for p in capacity['curve']], 'b', label='Capacity Curve')


    intersections = med_intersections + lower_intersections + upper_intersections
    # intersections
    plt.plot([p['x'] for p in intersections],
        [p['y'] for p in intersections], 'yo', label='Intersections')

    plt.xlim(0, xmax=demand[-1]['x'] * 2)
    plt.title('Performance Point Calculation')
    plt.xlabel('Spectral Displacement (inches)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.legend()

    impact_fig = plt.figure()
    plt.ylim(0, 1)
    n, s, m, e, c = plt.bar([1,2,3,4,5], [damage_probs['none'], damage_probs['slight'], damage_probs['moderate'], damage_probs['extensive'] + .01, damage_probs['complete'] + .01])
    n.set_facecolor('gray')
    s.set_facecolor('g')
    m.set_facecolor('gold')
    e.set_facecolor('orange')
    c.set_facecolor('r')
    plt.title('Potential Impact')

    return pp_fig, impact_fig

def main():
    pp_fig, impact_fig = run()
    plt.show()

if __name__ == '__main__':
    main()