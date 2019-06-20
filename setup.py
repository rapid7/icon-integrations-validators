#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='insightconnect_integrations_validators',
      version='0.1.0',
      description='Validator tooling for InsightConnect integrations',
      author='Rapid7 Integrations Alliance',
      author_email='integrationsalliance@rapid7.com',
      url='https://github.com/rapid7/icon-integrations-validators',
      packages=find_packages(),
      install_requires=[
          'validators==0.12.1',
          'filetype==1.0.0',
          'pathlib==1.0.1'
      ],
      license="MIT"
      )
