#!/usr/bin/env python
"""
MultiQC plugin for BLR
"""

from setuptools import setup, find_packages

version = '0.1'

setup(
    name='multiqc_blr',
    version=version,
    author='Pontus Höjer',
    description="MultiQC plugin for BLR",
    long_description=__doc__,
    keywords='bioinformatics',
    url='https://github.com/pontushojer/MultiQC_BLR',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'multiqc'
    ],
    entry_points={
        'multiqc.modules.v1': [
            'stats = multiqc_blr.modules.stats:MultiqcModule',
            "hapcut2 = multiqc_blr.modules.hapcut2:MultiqcModule",
        ],
        'multiqc.cli_options.v1': [
            'disable_plugin = multiqc_blr.cli:disable_plugin'
        ],
        'multiqc.hooks.v1': [
            'execution_start = multiqc_blr.multiqc_blr:execution_start'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
