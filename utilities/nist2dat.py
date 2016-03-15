#! /usr/bin/env python

###############################################################################
#                                                                             #
# (c) Adam Jackson 2016. This file is part of GAPTAP.                         #
#                                                                             #
# GAPTAP is free software: you can redistribute it and/or modify              #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# Foobar is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.             #
#                                                                             #
###############################################################################

from __future__ import print_function
import argparse
import numpy as np

try:
    from itertools import izip as zip
except ImportError:
    pass


def main(input_file, output_file=False, zpe=0, zpe_unit='kJ/mol', Tr=298.15):
    """Convert NIST/JANAF-like data table to chemical potential correction

    The expected file format has the following whitespace-separated
    columns, with fields indicated by the following two header lines:

    T       Cp      S       -(G-H(Tr))/T    H-H_Tr  Delta_H Delta_G Log_Kf
    K       J/molK  J/molK  J/molK          kJ/mol  kJ/mol  kJ/mol  n/a

    args:
        input_file (str): Path to input data file
        output_file (str): Path to output data file. If False, write to
            standard output.
        zpe (float): Zero-point energy in kJ/mol
        zpe_unit
        Tr (float): Reference temperature used to offset H values
    """

    data_table = np.genfromtxt(input_file, skip_header=2)
    T = data_table[:, 0]
    S = data_table[:, 2]
    H_from_zero = data_table[:, 4] - data_table[0, 4]
    G_from_zero = H_from_zero - (T * (S * 1e-3))
    mu = zpe * unit_to_kJmol(zpe_unit) + G_from_zero

    if output_file:
        with open(output_file, 'w') as f:
            f.writelines(line_printer(T, mu, newlines=True))
    else:
        for line in line_printer(T, mu):
            print(line)

def unit_to_kJmol(unit='kJmol'):
    """Conversion factors to kJmol.

    Derived from the Scipy physical constants library, which uses
    the 2010 CODATA recommended values.
    """
    if unit in ('kJmol', 'kJ/mol', 'kJmol-1'):
        return 1.
    elif unit in ('Jmol', 'J/mol', 'Jmol-1'):
        return 1e3
    elif unit in ('eV'):
        return 96.485336
    elif unit in ('cm-1', '/cm', 'cm'):
        return 0.0119627
    else:
        raise Exception("Unit '{0}' not known.".format(unit))

def line_printer(T, mu, filename=False, newlines=False):
    """Pretty print iterator"""
    if newlines:
        sep = '\n'
    else:
        sep = ''
    
    yield "       T/K           mu/kJ{0}".format(sep)

    for t, m in zip(T, mu):
        yield "{0:10.2f}\t{1:10.4f}{2}".format(t, m, sep)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('nist_file', type=str,
                        help="NIST/JANAF-like data file")
    parser.add_argument('zpe', type=float,
                        help="Zero-point energy in kJ/mol")
    parser.add_argument('--zpe_unit', type=str, default='eV',
                        help="Units for zero-point energy")
    parser.add_argument('-o', '--output_file', type=str, default=False,
                        help="Path to output .dat file for GAPTAP")
    args = parser.parse_args()

    main(args.nist_file, output_file=args.output_file,
         zpe=args.zpe, zpe_unit=args.zpe_unit)
