# -*- coding: utf-8 -*-

from os import path
from gaptap.model import Model
module_directory = path.abspath(path.dirname(__file__))
data_directory = path.join(module_directory, path.pardir, 'data')
default_config = path.join(data_directory, 'models.conf')

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


def get_config(filename=default_config):
    """
    Import config file

    Arguments
    ---------
    filename: str, optional
        Path of config file specifying data/models for materials

    Returns
    -------
    configparser.ConfigParser
        Object which is queried for configuation settings.

    """

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(filename)

    return config

# Automatically load all models into module namespace
# This allows materials to be loaded in Python with, e.g.
# import gaptap; o2_model = gaptap.O2
config = get_config()
for model in config.sections():
    if model == 'DEFAULTS':
        pass
    elif model in globals():
        raise Exception("Can't load model {0} from file as this would"
                        " cause namespace clash. Try renaming this section"
                        " in the config file".format(model))
    else:
        globals()[model] = Model(model, config=config)
