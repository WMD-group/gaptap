# -*- coding: utf-8 -*-
import gaptap
import numpy as np
from scipy.interpolate import interp1d

class Model(object):
    def __init__(self, id, config=None):
        if config and not config.has_section(id):
            raise Exception("Config file provided but model"
                            " '{0}' not found.".format(id))
        elif config:
            for option in config.options(id):
                setattr(self, option, config.get(id, option))

        if hasattr(self, 'property'):
            if self.property.decode('utf-8') == u'μ':
                self.property = 'mu'

            # if self.property == 'mu':
            #     def mu(self, T, **options):
            #         model_read_from_1D(self, T, **options)

def model_read_from_1D(model, T, **options):
    """
    Read data from 1D table file associated with Model

    The data format for these files is a pair of whitespace-separated
    columns.  The first column is the independent variable (usually
    Temperature) and the second column holds a thermodynamic property
    (usually μ). Comments are indicated with # character at start of
    line. Unicode characters and scientific notation are supported.

    e.g.
    # T/K    μ/kJ mol⁻¹
    0        20
    20       10.423
    50       -2.3e4

    Arguments
    ---------
    model : gaptap.model.Model
    
    T : number or ndarray
        T may be a scalar number type such as a
        float or a Numpy n-dimensional array.

    kind : str, optional
        Interpolation type. This is passed to scipy.interpolate.interp1d
        and accepts the same options (i.e. 'linear', 'nearest', 'zero',
        'slinear', 'quadratic', 'cubic')

    Returns
    -------
    numpy float or ndarray
        Interpolated values from tabulated data. If T is provided as an
        array, the return value is an array with the same shape.
    """
    return read_from_1D(T, model.data, **options)


def read_from_1D(T, table, kind='cubic'):
    """Read data from a 1D table file

    The data format for these files is a pair of whitespace-separated
    columns.  The first column is the independent variable (usually
    Temperature) and the second column holds a thermodynamic property
    (usually μ). Comments are indicated with # character at start of
    line. Unicode characters and scientific notation are supported.

    e.g.
    # T/K    μ/kJ mol⁻¹
    0        20
    20       10.423
    50       -2.3e4

    Arguments
    ---------
    T : number or ndarray
        T may be a scalar number type such as a
        float or a Numpy n-dimensional array.

    table: str
        Path to tabulated data

    kind: str, optional
        Interpolation type. This is passed to scipy.interpolate.interp1d
        and accepts the same options (i.e. 'linear', 'nearest', 'zero',
        'slinear', 'quadratic', 'cubic')

    Returns
    -------
    numpy float or ndarray
        Interpolated values from tabulated data. If T is provided as an
        array, the return value is an array with the same shape.

    """

    data = np.genfromtxt(table, comments='#', dtype=float)
    interp_function = interp1d(data[:, 0], data[:, 1], kind=kind)

    if type(T) in (list, tuple, np.ndarray):
        return interp_function(T)
    else:
        return interp_function(T).flatten()[0]
