import math
from . import sanaz
from .spectrum import build_spectrum, interpolate
from .data_tables import degradation_factor

def get_b_eff(capacity, kappa):
    last_b_h = 0
    b_eff_lst = [0] * len(capacity['curve'])
    b_eff_lst[0] = [{'x': 0, 'y': capacity['elastic_damping'] * 100}]

    for i in range(len(capacity['curve'])):
        point = capacity['curve'][i]

        if i > 0:
            prev_point = capacity['curve'][i - 1]
        else:
            prev_point = None

        t = 0
        if point['acc'] > 0:
            t = math.sqrt(point['disp'] /
                    (9.779738 * point['acc']))

        if t >= capacity['elastic_period'] and prev_point is not None:
            b_h = 100 * (kappa * ( 2*(point['acc'] + prev_point['acc']) *
                        (point['disp']-(prev_point['disp'] + (capacity['yield_point']['disp']/capacity['yield_point']['acc']) *
                        (point['acc']-prev_point['acc'])))+(((last_b_h/100)/kappa)) *
                        2 * math.pi * prev_point['disp']*prev_point['acc'])/(2*math.pi*point['disp']*point['acc']))

            last_b_h = b_h
          
            b_eff_lst[i] = {'x': t, 'y': max(b_h, capacity['elastic_damping'] * 100)}
        else:
            b_eff_lst[i] = {'x': t, 'y': (capacity['elastic_damping'] * 100)}

    return b_eff_lst

def get_dsf(beta, mag, rRup):
    dsf = []
    for i in range(len(beta)):
        lnDSF = ((sanaz.b0[i]['y'] + sanaz.b1[i]['y']*math.log(beta[i]['y']) + sanaz.b2[i]['y']*((math.log(beta[i]['y']))**2)) +
                        (sanaz.b3[i]['y'] + sanaz.b4[i]['y']*math.log(beta[i]['y']) + sanaz.b5[i]['y']*((math.log(beta[i]['y']))**2)) * mag +
                        (sanaz.b6[i]['y'] + sanaz.b7[i]['y']*math.log(beta[i]['y']) + sanaz.b8[i]['y']*((math.log(beta[i]['y']))**2)) * math.log(rRup+1))
        
        dsf += [{'x': beta[i]['x'], 'y': round(math.exp(lnDSF), 3)}]

    return dsf

def damp(demand, capacity, mag, r_rup):

    '''
    Histeretic damping spectrum and scale with dsf
    '''

    kappa = get_kappa(capacity['performance_rating'], capacity['year'], mag, r_rup)
    b_eff_spectrum = get_b_eff(capacity, kappa)

    beta = build_spectrum(b_eff_spectrum, sanaz.t)
    dsf = get_dsf(beta, mag, r_rup)

    # expand dsf to match demand spectrum periods
    dsf = build_spectrum(dsf, [point['period'] for point in demand])

    damped_demand = [0] * len(demand)
    for i in range(len(demand)):
        damp_disp = demand[i]['disp'] * dsf[i]['y']
        damp_acc = damp_disp/(9.779738 * demand[i]['period']**2)

        damped_demand[i] = {'disp': damp_disp, 'acc': damp_acc, 'period': demand[i]['period']}

    return damped_demand

def get_kappa(spr, year, mag, r_rup):
    if year > 1975:
        str_year = 'post-1975'
    elif year > 1960:
        str_year = '1960-1975'
    elif year > 1941:
        str_year = '1941-1959'
    else:
        str_year = 'pre-1941'

    if mag <= 6.25:
        str_mag = '<=6.25'
    elif mag <= 6.5:
        str_mag = '<=6.5'
        prev = '<=6.25'
        lower_mag = 6.25
        upper_mag = 6.5
    elif mag <= 6.75:
        str_mag = '<=6.75'
        prev = '<=6.5'
        lower_mag = 6.5
        upper_mag = 6.75
    elif mag <= 7:
        str_mag = '<=7'
        prev = '<=6.75'
        lower_mag = 6.75
        upper_mag = 7
    else:
        str_mag = '>=7.25'
        prev = '<=7'
        lower_mag = 7
        upper_mag = 7.25

    if r_rup <= 15:
        r_rup = int(round(r_rup))
    elif r_rup < 50:
        r_rup = int(round(r_rup / 5) * 5)
    elif r_rup < 1000:
        r_rup = 50
    else:
        r_rup = 1000

    spr = 'non-baseline' if spr != 'baseline' else spr

    if mag <= 6.25 or mag >= 7.25:
        kappa = degradation_factor[spr][str_year][str_mag][r_rup]
    else:
        kappa1 = degradation_factor[spr][str_year][prev][r_rup]
        kappa2 = degradation_factor[spr][str_year][str_mag][r_rup]

        point1 = {'x': lower_mag, 'y': kappa1}
        point2 = {'x': upper_mag, 'y': kappa2}

        kappa = interpolate(mag, point1, point2)

    return kappa
