#!/usr/bin/env python

"""Setup script"""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()
with open('requirements.txt') as requirement_file:
  requirements = requirement_file.read().splitlines()

setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest>=3', ]

setup(
    author="Vasil Papanchev",
    author_email='vasilpapanchev@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Implements REST APIs to send and receive messages using Peer-DIDs and the DIDComm Protocol.",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='didcommapi',
    name='aifb-did-communication-api',
    packages=find_packages(include=['did_communication_api', 'did_communication_api.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='',
    version='2.0.0',
    zip_safe=False,
)
