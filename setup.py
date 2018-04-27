#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# allow setup.py to be ran from anywhere
os.chdir(os.path.dirname(os.path.abspath(__file__)))

setup(
	name='diay',
	version='0.1',
	license='MIT',
	description='diay - a dependency injection library',
	author='Andreas Lutro',
	author_email='anlutro@gmail.com',
	url='https://github.com/anlutro/diay.py',
	packages=find_packages(include=('diay', 'diay.*')),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
	keywords=['dependency injection', 'inversion of control'],
)
