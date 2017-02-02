"""
GAPTAP: GAs Potentials over Temperature And Pressure
"""

from setuptools import setup, find_packages
from os import path

project_dir = path.abspath(path.dirname(__file__))

setup(
    name="gaptap",
    version="0.1.0",
    description="Thermodynamic potentials of gases from reference data",
    long_description="""
Obtain thermodynamic potentials for gas phases from reference data. Intended
for applications in ab initio chemical thermodynamics. Potential models include
metadata specifying reference states and data origin.""",
    url="https://github.com/wmd-group/gaptap",
    author="Adam J. Jackson",
    author_email="a.j.jackson@physics.org",
    license="GPL v3",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics'
        ],
    keywords="chemistry physics gas thermodynamics potential thermochemical",
    packages=find_packages(exclude=['bin', 'data', 'docs',
                                    'test', 'utilities']),
    install_requires=['numpy', 'scipy'],
    package_data={'galore': [path.join('data', 'data/*')]},
    scripts=[path.join('bin', 'gaptap')]
    )
