#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='kamado-bot',
      version='1.0',
      description='Standard music bot for discord',
      author='Lu Xinming',
      author_email='xinmingsm11@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        'discord',
        'youtube-dl'
        ],
     )