from .spectrum import build_spectrum
from . import damping

import math

def extend_demand(demand):
    '''
    Add a final point to the demand curve to anchor it and
    guarentee intersection with a capacity curve
    '''

    # Add final point to bring demand close to zero
    final_acc = .001
    final_disp = demand[-1]['disp'] * 3
    final_period = math.sqrt(final_disp / (final_acc * 9.779738))
    demand += [{
        'period': final_period,
        'acc': final_acc,
        'disp': final_disp
    }]

    return demand

def make_demand_spectrum(input, x='x', y='y'):
    '''
    Generate displacement values for a period/acceleration spectrum
    '''
    demand = []
    for point in input:
        disp = point[y] * point[x]**2 * 9.779738
        disp = disp if disp > 0 else 0
        acc = disp/(9.779738 * (point[x]**2))
        demand += [{
            'period': point[x],
            'acc': acc,
            'disp': disp
        }]

    return demand

def get_demand(hazard, hazard_beta, pref_periods, capacity, mag, rRup):
    '''
    Generate a displacement/SA spectrum from an input period/SA spectrum
    using a specific uncertainty, list of prefered periods, capacity
    magnitude and distance to the rupture
    '''
    output = build_spectrum(hazard, pref_periods, insert=[capacity['elastic_period'], capacity['ultimate_period']], finish_val=0)
    demand_spec = make_demand_spectrum(output)
    damped_demand = damping.damp(demand_spec, capacity, mag, rRup)

    demand = extend_demand(damped_demand)

    upper_bound_demand = []
    lower_bound_demand = []
    for point in demand:
        lower_bound_demand += [
            {
                'disp': point['disp'] / math.exp(hazard_beta),
                'acc': point['acc'] / math.exp(hazard_beta)
            }
        ]
        upper_bound_demand += [
            {
                'disp': point['disp'] * math.exp(hazard_beta),
                'acc': point['acc'] * math.exp(hazard_beta)
            }
        ]

    return demand, lower_bound_demand, upper_bound_demand
