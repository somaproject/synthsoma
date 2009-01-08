#/usr/bin/env python
from distutils.core import setup

setup(name="SyntheticSoma",
	author = "Stuart Layton",
	author_email = "slayton@mit.edu",
	url = "http://soma.mit.edu",
	version = "1.0",
	packages = ['synthsoma', 'somaLib'],
	package_dir = {'synthsoma': "synthsoma"},
	package_dir = {'somaLib': "synthsoma/somaLib"},
	scripts = ['runSynthSoma']
	)
