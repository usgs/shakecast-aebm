import unittest

from shakecastaebm.performance_point import *

class TestGetPerformancePoint(unittest.TestCase):
    def test_performancePoint(self):
        capacity = [
            {'disp': 1, 'acc': .1},
            {'disp': 2, 'acc': 1}
        ]
        demand = [
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': .1}
        ]

        pp = get_performance_point(capacity, demand)
        self.assertTrue(isinstance(pp, list))

        pp = pp[0]
        self.assertTrue('disp' in pp.keys())
        self.assertTrue('acc' in pp.keys())
        self.assertTrue('period' in pp.keys())

    def test_intersection(self):
        capacity = [
            {'disp': 1, 'acc': .1},
            {'disp': 2, 'acc': 1}
        ]
        demand = [
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': .1}
        ]

        pp = get_performance_point(capacity, demand)[0]

        # slopes for the intersection with the demand
        dem_slope1 = ((demand[0]['acc'] - pp['acc']) /
                (demand[0]['disp'] - pp['disp']))
        dem_slope2 = ((demand[1]['acc'] - pp['acc']) /
                (demand[1]['disp'] - pp['disp']))
        
        # slopes for intersection with capacity
        cap_slope1 = ((capacity[0]['acc'] - pp['acc']) /
                (capacity[0]['disp'] - pp['disp']))
        cap_slope2 = ((capacity[1]['acc'] - pp['acc']) /
                (capacity[1]['disp'] - pp['disp']))

        self.assertAlmostEqual(dem_slope1, dem_slope2)
        self.assertAlmostEqual(cap_slope1, cap_slope2)


if __name__ == '__main__':
    unittest.main()
