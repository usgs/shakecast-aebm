import matplotlib.pyplot as plt

from shakecastaebm.performance_point import performance_point
from shakecastaebm.demand import get_demand, make_demand_spectrum
from shakecastaebm.spectrum import build_spectrum
from shakecastaebm.damage import *
from shakecastaebm.capacity import get_capacity
from shakecastaebm.damping import get_kappa, get_b_eff, get_dsf
from shakecastaebm.core import run as run_aebm
from shakecastaebm.data_tables import pref_periods
from shakecastaebm.sanaz import t as sanaz_t
from .data import *

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
    output = build_spectrum(hazard, pref_periods, insert=[capacity['elastic_period'], capacity['ultimate_period']], finish_val=0)
    undamped_demand = make_demand_spectrum(output)

    kappa = get_kappa(capacity['performance_rating'], capacity['year'], mag, r_rup)
    b_eff = get_b_eff(capacity, kappa)

    beta = build_spectrum(b_eff, sanaz_t)
    dsf = get_dsf(beta, mag, r_rup)

    (damage_probs,
    capacity,
    demand,
    lower_demand,
    upper_demand,
    med_intersections,
    lower_intersections,
    upper_intersections) = run_aebm(capacity,
            hazard, hazard_beta, mag, r_rup)

    cap_fig = plt.figure()
    plt.plot([p['x'] for p in capacity['curve']],
        [p['y'] for p in capacity['curve']], 'b', label='Capacity Curve')
    plt.xlabel('Spectral Displacement (inches)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.title('Capacity Curve')
    plt.xlim(0, 10)

    haz_fig = plt.figure()
    plt.title('Input Hazard')
    plt.plot([p['x'] for p in hazard], [p['y'] for p in hazard], 'o', label='Input Hazard')
    plt.plot([p['x'] for p in output], [p['y'] for p in output], label='Expanded Hazard')
    plt.xlabel('Period (s)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.legend()

    dsf_fig = plt.figure()
    plt.title('DSF Curve')
    plt.plot([p['x'] for p in dsf], [p['y'] for p in dsf])
    plt.xlabel('Period (s)')
    plt.ylabel('DSF')
    plt.legend()

    dem_fig = plt.figure()
    plt.title('Demand Curve')
    plt.plot([p['disp'] for p in undamped_demand], [p['y'] for p in undamped_demand], label='Raw Demand')
    plt.plot([p['disp'] for p in demand], [p['y'] for p in demand], label='Damped Demand')
    plt.xlabel('Spectral Displacement (inches)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.xlim(0, xmax=demand[-1]['x'] * 2)
    plt.legend()

    pp_fig = plt.figure()
    plt.plot([p['disp'] for p in demand],
        [p['y'] for p in demand], '-r', label='Median Demand')
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
    plt.title('Performance Point Calculation\nDemand: {0:.2f} in, Spectral Acceleration: {0:.2f} %g'.format(med_intersections[0]['x'], med_intersections[0]['y']))
    plt.xlabel('Spectral Displacement (inches)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.legend()

    impact_fig = plt.figure()
    plt.ylim(0, 100)
    n, s, m, e, c = plt.bar(
        [1, 2, 3, 4, 5], 
        [
            damage_probs['none'] * 100,
            damage_probs['slight'] * 100,
            damage_probs['moderate'] * 100,
            damage_probs['extensive'] * 100,
            damage_probs['complete'] * 100
        ]
    )
    n.set_facecolor('gray')
    s.set_facecolor('g')
    m.set_facecolor('gold')
    e.set_facecolor('orange')
    c.set_facecolor('r')
    plt.ylabel('Probability of Exceedance (%)')
    plt.title('Potential Impact')
    plt.xticks([1,2,3,4,5], ['None', 'Slight', 'Moderate', 'Extensive', 'Complete'])

    return cap_fig, haz_fig, dsf_fig, dem_fig, pp_fig, impact_fig

def main():
    plots = run()
    plt.show()

if __name__ == '__main__':
    main()