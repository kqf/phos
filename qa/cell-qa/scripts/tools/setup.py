from setuptools import setup, find_packages

setup(
    name="phosqa",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tofqa=phosqa.tof:main',
            'tofqa-distribution=phosqa.tof:distribution',
            'trending=phosqa.trending:main',
            'xz2abs=phosqa.xz:main',
        ],
    },
)
