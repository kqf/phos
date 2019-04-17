from setuptools import setup, find_packages

setup(
    name="drawtools",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'style=drawtools.style:main',
            'badmaps=drawtools.badmap:main',
            "fdiff=drawtools.filediff:main"
        ],
    },
)
