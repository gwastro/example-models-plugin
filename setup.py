#!/usr/bin/env python
"""
Example setup file for PyCBC plugin models.
"""

from setuptools import setup

VERSION = '0.0.dev0'
NAME = 'pycbc_poisson_models'

setup (
    name = NAME,
    version = VERSION,
    description = 'Example plugin models for PyCBC',
    author = 'The PyCBC team',
    author_email = 'cdcapano@gmail.com',
    url = 'http://www.pycbc.org/',
    download_url = 'https://github.com/gwastro/example-models-plugin/tarball/v%s' % VERSION,
    keywords = ['pycbc', 'bayesian inference', 'gravitational waves',
                'multimessenger astronomy'],
    install_requires = ['pycbc'],
    py_modules = ['pycbc_poisson_models'],
    entry_points = {
        "pycbc.inference.models": ["test_poisson = pycbc_poisson_models:TestPoisson",
                                   "poisson_burst = pycbc_poisson_models:PoissonBurst",
                                   "poisson_burst2 = pycbc_poisson_models:PoissonBurst2",
                                   ]
        },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        ],
)
