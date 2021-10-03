#!/usr/bin/env python3
# setup.py
import os
from setuptools import setup, find_packages, Extension
from distutils.command.build import build


class Build(build):
    def finalize_options(self):
        super().finalize_options()
        from Cython.Build import cythonize
        self.distribution.ext_modules = cythonize(self.distribution.ext_modules)


with open('README.md', 'r') as file:
    LONG_DESCRIPTION = file.read()

with open('LICENSE.txt', 'r') as file:
    LICENSE = file.read()

DESCRIPTION = 'InvisibleCharm is a python script that allows you to hide your files.'
VERSION = '2.3.0'
REQUIREMENTS = ['log21', 'Pillow', 'pycryptodome', 'importlib_resources']
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
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    setup_requires=["cython"],
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
    include_package_data=True,
    cmdclass={"build": Build}
)
