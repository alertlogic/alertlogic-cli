from distutils.core import setup
from setuptools import find_packages
VERSION = '1.2.0'
setup(
    name = 'alertlogic_cli',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    scripts = ['alertlogic-cli'],
    version = VERSION,
    license='MIT',
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    description = 'Command Line Client for Alertlogic Services.',
    author = 'Alert Logic Inc.',
    author_email = 'support@alertlogic.com',
    url = 'https://github.com/alertlogic/alertlogic-cli',
    download_url = "https://github.com/alertlogic/alertlogic-cli/archive/%s.tar.gz" % (VERSION),
    keywords = ['cli', 'alertlogic'],
    classifiers = [],
)