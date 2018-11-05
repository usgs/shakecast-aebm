import unittest

from shakecastaebm.capacity import get_capacity
from shakecastaebm.core import run

class TestRun(unittest.TestCase):
    def test_Runs(self):
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
        
        results = run(capacity,
                hazard, hazard_beta, mag, r_rup)

        for result in results:
            self.assertIsNotNone(result)

    def test_LargeHazardSmallCapacity(self):
        # run shakecast example
        hazard = [
            {'x': .03, 'y': 3.0},
            {'x': 1.0, 'y': 2.5},
            {'x': 3.0, 'y': 1.4}
        ]

        hazard_beta = .5
        mag = 6.7
        r_rup = 20

        capacity = get_capacity('C2', 'low', 1, 24, 2, 1990, 'very_poor', 'poor')

        results = run(capacity,
                hazard, hazard_beta, mag, r_rup)

        for result in results:
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
    