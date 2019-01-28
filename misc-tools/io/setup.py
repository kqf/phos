from setuptools import setup, find_packages

setup(
    name="phosio",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'unlist=phosio.main:munlist',
            'remove2dir=phosio.main:mremove2dir',
        ],
    },
)
