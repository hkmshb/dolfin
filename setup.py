# -*- coding: utf-8 -*-
import os
from setuptools import setup
import dolfin


setup(
    name='dolfin',
    version=dolfin.__version__,

    author=dolfin.__author__,
    author_email='info@hazeltek.com',
    url='http://hazeltek.com/',
    description='A python general purpose utility library',
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.md')).read(),

    py_modules=['dolfin'],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
)
