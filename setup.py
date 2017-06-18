# -*- coding: utf-8 -*-


import os
from setuptools import setup, find_packages


exec(open(os.path.join('dynaremd', '__init__.py')).read())


setup(
    name='dynaremd',
    version=VERSION,

    description='Markdown pre-processor for Dynare',
    long_description=open('README.md').read(),

    url='https://github.com/ChrisThoung/dynare-markdown',

    author='Chris Thoung',
    author_email='chris.thoung@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='economics macroeconomics dynare markdown',

    packages=find_packages(),
)
