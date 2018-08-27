import os
import sys

from . import shakecast
from . import workbook
from . import damping
from . import demand

def main(path='.'):
    pp_fig, capacity_fig, acc_diff_fig, disp_diff_fig = workbook.run()
    cap_fig, haz_fig, dsf_fig, dem_fig, sc_pp_fig, impact_fig = shakecast.run()
    damp1, damp2 = damping.run()
    demand1, demand2 = demand.run()

    if not os.path.exists(path):
        os.makedirs(path)

    # save workbook validation figures
    pp_fig.savefig(os.path.join(path, 'perf_point1'))
    capacity_fig.savefig(os.path.join(path, 'capacity_comp'))
    acc_diff_fig.savefig(os.path.join(path, 'acc_diff'))
    disp_diff_fig.savefig(os.path.join(path, 'disp_diff'))

    # save shakecast figures
    cap_fig.savefig(os.path.join(path, 'sc_capacity'))
    haz_fig.savefig(os.path.join(path, 'sc_hazard'))
    dsf_fig.savefig(os.path.join(path, 'sc_dsf'))
    dem_fig.savefig(os.path.join(path, 'sc_demand'))
    sc_pp_fig.savefig(os.path.join(path, 'perf_point2'))
    impact_fig.savefig(os.path.join(path, 'impact_fig'))

    # save damping figures
    damp1.savefig(os.path.join(path, 'damping_beta'))
    damp2.savefig(os.path.join(path, 'damping_dsf'))

    # save demand figures
    demand1.savefig(os.path.join(path, 'hazard_expansion'))
    demand2.savefig(os.path.join(path, 'damped_demand'))

if __name__ == '__main__':
    path = '.'
    if len(sys.argv) > 1:
        path = sys.argv[1]

    main(path)
