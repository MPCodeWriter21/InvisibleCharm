#!/usr/bin/env python3
# setup.py
import InvisibleCharm.Settings
from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

DESCRIPTION = ''
VERSION = '2.0.0'
REQUIREMENTS = ['log21', 'Pillow', 'pycryptodome']
if InvisibleCharm.Settings.is_windows:
    REQUIREMENTS.append('python-magic-bin')
else:
    REQUIREMENTS.append('python-magic')

setup(
    name='InvisibleCharm',
    version=VERSION,
    url='https://github.com/MPCodeWriter21/InvisibleCharm',
    author='CodeWriter21(Mehrad Pooryoussof)',
    author_email='<CodeWriter21@gmail.com>',
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
    keywords=['python', 'python3', 'CodeWriter21'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
