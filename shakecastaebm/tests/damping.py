import unittest

from shakecastaebm.capacity import get_capacity
from shakecastaebm.damping import *
from shakecastaebm.demand import make_demand_spectrum

class TestKappa(unittest.TestCase):
    def test_validate(self):
        kappa = get_kappa('baseline', 1971, 6.5, 20)
        self.assertAlmostEqual(kappa, .6)

        kappa = get_kappa('poor', 1961, 6.5, 20)
        self.assertAlmostEqual(kappa, .4)

        kappa = get_kappa('baseline', 1990, 7.9, 11.2)
        self.assertAlmostEqual(kappa, .7)

        kappa = get_kappa('very_poor', 1990, 7.9, 11.2)
        self.assertAlmostEqual(kappa, .5)

        kappa = get_kappa('very_poor', 1955, 7.9, 11.2)
        self.assertAlmostEqual(kappa, .3)

        kappa = get_kappa('very_poor', 1940, 7.9, 11.2)
        self.assertAlmostEqual(kappa, .2)

        kappa = get_kappa('very_poor', 1940, 3, 11.2)
        self.assertAlmostEqual(kappa, .35)

        kappa = get_kappa('very_poor', 1940, 6.75, 11.2)
        self.assertAlmostEqual(kappa, .25)

        kappa = get_kappa('very_poor', 1940, 7, 11.2)
        self.assertAlmostEqual(kappa, .23)


class TestDamp(unittest.TestCase):
    def test_runs(self):
        hazard = [
            {'x': .03, 'y': 1.1377},
            {'x': 1.0, 'y': .8302},
            {'x': 3.0, 'y': .348}
        ]

        mag = 6.7
        r_rup = 20

        capacity = get_capacity('C2', 'high', 1, 24, 2, 1990, 'very_poor', 'poor')
        demand = make_demand_spectrum(hazard)
        damped_demand = damp(demand, capacity, mag, r_rup)

        for i in range(len(damped_demand) - 1):
            self.assertTrue(damped_demand[i]['acc'] <= demand[i]['acc'])


if __name__ == '__main__':
    unittest.main()