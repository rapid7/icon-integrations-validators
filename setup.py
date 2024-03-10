#!/usr/bin/env python
from icon_validator import VERSION
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="insightconnect_integrations_validators",
    version=VERSION,
    description="Validator tooling for InsightConnect integrations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rapid7 Integrations Alliance",
    author_email="integrationalliance@rapid7.com",
    url="https://github.com/rapid7/icon-integrations-validators",
    packages=find_packages(),
    install_requires=[
        "jsonschema==2.3.0",
        "validators==0.22.0",
        "filetype==1.0.5",
        "insightconnect-integrations-plugin-spec-tooling==1.3.2",
        "requests==2.31.0",
        "urlextract==0.14.0",
        "typing==3.7.4.1",
        "PyYAML==6.0.1",
        "dacite==1.6.0",
        "GitPython==3.1.41",
    ],
    entry_points={"console_scripts": ["icon-validate=icon_validator.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
    ],
    license="MIT",
)
