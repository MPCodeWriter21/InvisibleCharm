#!/usr/bin/env python3
# setup.py
import os
from setuptools import setup, find_packages, Extension


with open('README.md', 'r') as file:
    LONG_DESCRIPTION = file.read()

with open('LICENSE.txt', 'r') as file:
    LICENSE = file.read()

DESCRIPTION = 'InvisibleCharm is a python script that allows you to hide your files.'
VERSION = '2.4.1'
REQUIREMENTS = ['log21>=1.5.1', 'Pillow>=8.3.2', 'pycryptodome>=3.12.0', 'importlib_resources>=5.2.2']
if os.name == 'nt':
    REQUIREMENTS.append('python-magic-bin>=0.4.14')
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
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    setup_requires=["cython>=0.29.24"],
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'InvisibleCharm = InvisibleCharm:entry_point'
        ]
    },
    ext_modules=[Extension(name='InvisibleCharm.lib.operations.Image',
                           sources=['InvisibleCharm/lib/operations/Image.pyx'])],
    keywords=['python', 'python3', 'CodeWriter21', 'Hide', 'Hidden', 'InvisibleCharm', 'Invisible', 'Charm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
    include_package_data=True
)
