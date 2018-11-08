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
        self.assertTrue(isinstance(pp, dict))
        self.assertTrue('disp' in pp.keys())
        self.assertTrue('acc' in pp.keys())
        self.assertTrue('period' in pp.keys())

    def test_Intersection(self):
        capacity = [
            {'disp': 1, 'acc': .1},
            {'disp': 2, 'acc': 1}
        ]
        demand = [
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': .1}
        ]

        pp = get_performance_point(capacity, demand)

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

    def test_TripleIntersection(self):
        capacity = [
            {'disp': .1, 'acc': 1},
            {'disp': .5, 'acc': 1},
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': 1},
            {'disp': 3, 'acc': 1},
            {'disp': 4, 'acc': 1}
        ]

        demand = [
            {'disp': .1, 'acc': 2},
            {'disp': .5, 'acc': .5},
            {'disp': 2, 'acc': 1.5},
            {'disp': 3, 'acc': .1}
        ]

        perf_point = get_performance_point(capacity, demand)
        intersections = find_intersections(capacity, demand, 'disp', 'acc')

        self.assertTrue(perf_point is not None)
        self.assertTrue(perf_point['disp'] < intersections[-1]['disp'])

    def test_ChopCurve(self):
        curve = [
            {'disp': .1, 'acc': 1},
            {'disp': .5, 'acc': 1},
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': 1},
            {'disp': 3, 'acc': 1},
            {'disp': 4, 'acc': 1}
        ]

        start = .3
        end = 2.2

        chopped = chop_curve(curve, start, end, 'disp', 'acc')

        self.assertAlmostEqual(start, chopped[0]['disp'])
        self.assertAlmostEqual(end, chopped[-1]['disp'])

    def test_FindPointOnCurve(self):
        curve = [
            {'disp': .1, 'acc': 1},
            {'disp': .5, 'acc': 1},
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': 1},
            {'disp': 3, 'acc': 1},
            {'disp': 4, 'acc': 1}
        ]

        point_disp = 1.7
        point = find_point_on_curve(point_disp, curve, 'disp', 'acc')

        self.assertAlmostEqual(point_disp, point['disp'])
        self.assertAlmostEqual(1, point['acc'])

    def test_FindPointOnCurveLastSegment(self):
        curve = [
            {'disp': .1, 'acc': 1},
            {'disp': .5, 'acc': 1},
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': 1},
            {'disp': 3, 'acc': 1},
            {'disp': 4, 'acc': 1}
        ]

        point_disp = 3.8
        point = find_point_on_curve(point_disp, curve, 'disp', 'acc')

        self.assertAlmostEqual(point_disp, point['disp'])

    def test_GetAreaUnderCurve(self):
        curve = [
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': 1},
            {'disp': 3, 'acc': 1},
            {'disp': 4, 'acc': 1}
        ]

        area = get_area_under_curve(curve, 'disp', 'acc')
        EXPECTED_AREA = 3

        self.assertAlmostEqual(area, EXPECTED_AREA)

    def test_FindsIntersectionInLastSegment(self):
        capacity = [
            {'disp': 1, 'acc': 1},
            {'disp': 2, 'acc': 1},
            {'disp': 3, 'acc': 1},
            {'disp': 4, 'acc': 1}
        ]

        demand = [
            {'disp': 1, 'acc': 2},
            {'disp': 2, 'acc': 2},
            {'disp': 3, 'acc': 2},
            {'disp': 4, 'acc': 0}
        ]

        pp = get_performance_point(capacity, demand)
        self.assertIsNotNone(pp)

if __name__ == '__main__':
    unittest.main()
