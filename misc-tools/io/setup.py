from setuptools import setup, find_packages

setup(
    name="phosio",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "unlist=phos.main:munlist",
            "remove2dir=phos.main:mremove2dir",
            "phos-download=phos.download:main",
        ],
    },
)
