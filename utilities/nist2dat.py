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
from scipy import constants

try:
    from itertools import izip as zip
except ImportError:
    pass


def main(input_file, output_file=False, zpe=0, zpe_unit='kJ/mol', Tr=298.15,
         frequencies=[], freq_unit='cm-1'):
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

    if frequencies:
        zpe = zpe_from_frequencies(frequencies, freq_unit=freq_unit)
        zpe_unit = 'Jmol'

    mu = zpe * unit_to_kJmol(zpe_unit) + G_from_zero

    if output_file:
        with open(output_file, 'w') as f:
            f.writelines(line_printer(T, mu, newlines=True))
    else:
        for line in line_printer(T, mu):
            print(line)

def unit_to_kJmol(unit):
    """Conversion factors to kJmol.

    Derived from the Scipy physical constants library, which uses
    the 2010 CODATA recommended values.
    """
    if unit in ('kJmol', 'kJ/mol', 'kJmol-1'):
        return 1.
    elif unit in ('Jmol', 'J/mol', 'Jmol-1'):
        return 1e-3
    elif unit in ('eV'):
        return 96.485336
    elif unit in ('cm-1', '/cm', 'cm'):
        return 0.0119627
    else:
        raise Exception("Unit '{0}' not known.".format(unit))

def unit_to_Hz(unit):
    """Conversion factors for frequency units to Hz (s-1)"""
    if unit in ('Hz', 's-1', '/s'):
        return 1.
    elif unit in ('m-1', '/m', 'm'):
        return constants.c
    elif unit in ('cm-1', '/cm', 'cm'):
        return unit_to_Hz('m-1') * 1e2
    elif unit in ('rad/s', 'rads-1', 'rads', 'w'):
        return 1./(2. * constants.pi)
    else:
        raise Exception("Unit '{0}' not known.".format(unit))    

def line_printer(T, mu, filename=False, newlines=False):
    """Pretty print iterator"""
    if newlines:
        sep = '\n'
    else:
        sep = ''
    
    yield "     T / K     mu / kJmol-1{0}".format(sep)

    for t, m in zip(T, mu):
        yield "{0:10.2f}\t{1:10.4f}{2}".format(t, m, sep)

def zpe_from_frequencies(frequencies, freq_unit='cm-1'):
    """ZPE of a molecule in J/mol from frequency list

    The zero-point energy of an oscillator e = hv/2"""
    return product(constants.h, 0.5, unit_to_Hz(freq_unit),
                   sum(frequencies), constants.N_A)

def product(*args):
    """Multiply an arbitrary number of arguments"""
    return reduce(lambda x,y: x * y, args, 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('nist_file', type=str,
                        help="NIST/JANAF-like data file")
    parser.add_argument('--zpe', type=float, default=0.,
                        help="Zero-point energy")
    parser.add_argument('--zpe_unit', type=str, default='eV',
                        help="Units for zero-point energy")
    parser.add_argument('-o', '--output_file', type=str, default=False,
                        help="Path to output .dat file for GAPTAP")
    parser.add_argument('-f', '--frequencies', type=float, nargs='*',
                        help="List of frequencies for ZPE computation")
    parser.add_argument('--freq_unit', type=str, default='cm-1',
                        help="Units for vibrational frequencies")
    args = parser.parse_args()

    main(args.nist_file, output_file=args.output_file,
         zpe=args.zpe, zpe_unit=args.zpe_unit,
         frequencies=args.frequencies, freq_unit=args.freq_unit)
