#! /usr/bin/env python

import unittest
import gaptap
from gaptap.model import read_from_1D
import numpy as np
from os import path

from numpy.testing import assert_allclose


class Test1DFileImporter(unittest.TestCase):
    def setUp(self):
        self.o2_file = path.join(gaptap.data_directory, 'O2.dat')
        self.T_values = [[0, 100, 300], [1000, 1100, 1300]]

    def test_read_from_1D(self):
        assert_allclose(read_from_1D(self.T_values, self.o2_file),
                        np.array([[9.4192, -5.0075, -43.4425],
                                  [-202.7728, -227.3000, -277.2952]]))

    def test_shape_from_1D(self):
        self.assertEqual(np.shape(read_from_1D(self.T_values,
                                               self.o2_file)),
                         (len(self.T_values), len(self.T_values[0])))

    def test_linear_interp_1D(self):
        self.assertAlmostEqual((sum(read_from_1D([100, 200],
                                                 self.o2_file)))/2,
                               read_from_1D(150, self.o2_file,
                                            kind='linear'))


if __name__ == '__main__':
    unittest.main()
