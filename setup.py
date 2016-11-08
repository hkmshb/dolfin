# -*- coding: utf-8 -*-
import os
from setuptools import setup
import dolfin


setup(
    name='dolfin',
    version=dolfin.__version__,
    zip_safe=False,

    author=dolfin.__author__,
    author_email='info@hazeltek.com',
    maintainer='Abdul-Hakeem Shaibu',
    maintainer_email='hkmshb@gmail.com',
    url='https://github.com/hkmshb/dolfin',
    description='A python general purpose utility library',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.md')).read(),

    packages=['dolfin', 'dolfin.ext'],
    platforms='any',
    classifiers=[
        'Development Status :: *',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: ISV',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)
