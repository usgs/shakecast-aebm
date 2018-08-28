import matplotlib.pyplot as plt

from shakecastaebm.performance_point import performance_point
from shakecastaebm.demand import get_demand
from shakecastaebm.spectrum import build_spectrum
from shakecastaebm.damage import *
from shakecastaebm.capacity import *
from shakecastaebm.core import run as run_aebm
from shakecastaebm.data_tables import pref_periods
from .data import *


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def run():
    capacity = get_capacity('PC1', 'high', 7, 24, 2, 1990, 'very_poor', 'poor')
    (damage_probs,
    capacity,
    demand,
    lower_demand,
    upper_demand,
    med_intersections,
    lower_intersections,
    upper_intersections) = run_aebm(capacity,
            hazard, hazard_beta, mag, r_rup)

    pp_fig = plt.figure()
    plt.xlim(xmin=0)
    plt.plot([p['disp'] for p in demand],
        [p['y'] for p in demand], '-ro', label='Calculated Demand')
    plt.plot([p['disp'] for p in upper_demand],
        [p['y'] for p in upper_demand], label='Upper bound demand')
    plt.plot([p['disp'] for p in lower_demand],
        [p['y'] for p in lower_demand], label='Lower bound demand')
    plt.plot([p['x'] for p in capacity['curve']],
        [p['y'] for p in capacity['curve']], 'b', label='Capacity Curve')
    plt.plot([p['disp'] for p in demand_check],
        [p['y'] for p in demand_check], '-go', label='Demand Verification')


    intersections = med_intersections + lower_intersections + upper_intersections
    # intersections
    plt.plot([p['x'] for p in intersections],
        [p['y'] for p in intersections], 'yo', label='Intersections')

    plt.xlim(xmax=demand[-1]['x'] * 2)
    plt.title('Performance Point Workbook Verification')
    plt.xlabel('Spectral Displacement (inches)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.legend()

    capacity_fig = plt.figure()
    plt.title('Capacity Curve Workbook Verification')
    plt.xlabel('Spectral Displacement (inches)')
    plt.ylabel('Spectral Acceleration (%g)')
    plt.plot([p['x'] for p in capacity['curve']],
    [p['y'] for p in capacity['curve']], '-ob', label='Computed Capacity Curve')
    plt.plot(capacity_x, capacity_y, 'r', label='Capacity Curve Verification')

    plt.xlim(0, 10)
    plt.legend()

    acc_diff_fig = plt.figure()
    acc_difs = []
    for dem in demand:
        for c in demand_check:
            if isclose(c['x'], dem['x']):
                acc_difs += [{'x': dem['x'], 'y': (c['y'] - dem['y'])/c['y']}]
                break

    plt.plot([p['x'] for p in acc_difs], [p['y'] for p in acc_difs], 'o')
    
    plt.title('Demand Acceleration Difference (vs. workbook)')
    plt.xlabel('Period (s)')
    plt.ylabel('Difference Ratio')

    disp_diff_fig = plt.figure()
    disp_difs = []
    acc_difs = []
    for dem in demand:
        for c in demand_check:
            if isclose(c['x'], dem['x']):
                diff = (c['disp'] - dem['disp'])
                ratio = 0 if diff < .001 else diff / c['disp']

                disp_difs += [{'x': dem['x'], 'y': ratio}]
                break
  
    plt.plot([p['x'] for p in disp_difs][1:], [p['y'] for p in disp_difs][1:], 'o')
    
    plt.title('Demand Displacement Difference (vs. workbook)')
    plt.xlabel('Period (s)')
    plt.ylabel('Difference Ratio')

    return pp_fig, capacity_fig, acc_diff_fig, disp_diff_fig

def main():
    pp_fig, capacity_fig, acc_diff_fig, disp_diff_fig = run()
    plt.show()

if __name__ == '__main__':
    main()
