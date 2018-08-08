import unittest

from shakecastaebm.damping import *

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

if __name__ == '__main__':
    unittest.main()