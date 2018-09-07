import unittest

from shakecastaebm.spectrum import *

class TestBuildSpectrum(unittest.TestCase):
    def setUp(self):
        self.line = [
            {'x': 0, 'y': 1},
            {'x': 1, 'y': 1}
        ]
        self.pref = [.1, .2, .3, .4, .5, .6, .7, .8, .9]

    def test_buildsDefaults(self):
        expanded_line = build_spectrum(self.line, self.pref)

        self.assertTrue(len(expanded_line) == len(self.pref))
        for point in expanded_line:
            self.assertTrue(point['x'] in self.pref)


    def test_buildsDisorderedInput(self):
        line = list(reversed(self.line))
        expanded_line = build_spectrum(line, self.pref)

        last = expanded_line[0]['x'] - 1
        for point in expanded_line:
            self.assertTrue(last < point['x'])
            last = point['x']

    def test_insertVals(self):
        insert = [.25, .45]
        expanded_line = build_spectrum(self.line, self.pref, insert=insert)

        all_xs = [p['x'] for p in expanded_line]
        for x in insert:
            self.assertTrue(x in all_xs)

    def test_usesDefinedXandY(self):
        new_line = [{'cus': p['x'], 'tom': p['y']} for p in self.line]
        normal_line = build_spectrum(self.line, self.pref)
        custom_line = build_spectrum(new_line, self.pref, x='cus', y='tom')

        for i in range(len(normal_line)):
            self.assertEqual(normal_line[i]['x'], custom_line[i]['cus'])
            self.assertEqual(normal_line[i]['y'], custom_line[i]['tom'])

if __name__ == '__main__':
    unittest.main()