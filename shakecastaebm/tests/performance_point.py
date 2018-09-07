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

def main():
    unittest.main()

if __name__ == '__main__':
    main()