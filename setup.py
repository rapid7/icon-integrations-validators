#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='insightconnect_integrations_validators',
      version='1.3.0',
      description='Validator tooling for InsightConnect integrations',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Rapid7 Integrations Alliance',
      author_email='integrationalliance@rapid7.com',
      url='https://github.com/rapid7/icon-integrations-validators',
      packages=find_packages(),
      install_requires=[
          'python_jsonschema_objects==0.3.2',
          'jsonschema==2.3.0',
          'validators==0.12.1',
          'filetype==1.0.0',
          'pathlib==1.0.1',
          'insightconnect-integrations-plugin-spec-tooling~=1.0'
      ],
      entry_points={
        'console_scripts': [
            'icon-validate=icon_validator.__main__:main'
        ]
      },
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools"
      ],
      license="MIT"
      )
