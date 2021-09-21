#!/usr/bin/env python3
# setup.py
import os
from setuptools import setup, find_packages
from Cython.Build import cythonize

with open('README.md', 'r') as file:
    long_description = file.read()

with open('LICENSE.txt', 'r') as file:
    LICENSE = file.read()

DESCRIPTION = 'InvisibleCharm is a python script that allows you to hide your files.'
VERSION = '2.2.0'
REQUIREMENTS = ['log21', 'Pillow', 'pycryptodome']
if os.name == 'nt':
    REQUIREMENTS.append('python-magic-bin')
else:
    REQUIREMENTS.append('python-magic')

setup(
    name='InvisibleCharm',
    version=VERSION,
    url='https://github.com/MPCodeWriter21/InvisibleCharm',
    author='CodeWriter21(Mehrad Pooryoussof)',
    author_email='<CodeWriter21@gmail.com>',
    license=LICENSE,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'InvisibleCharm = InvisibleCharm:entry_point'
        ]
    },
    ext_modules=cythonize('InvisibleCharm/lib/operations/Image.pyx'),
    keywords=['python', 'python3', 'CodeWriter21', 'Hide', 'Hidden', 'InvisibleCharm', 'Invisible', 'Charm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
    include_package_data=True
)
