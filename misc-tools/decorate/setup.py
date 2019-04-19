from setuptools import setup, find_packages

setup(
    name="drawtools",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "style=drawtools.style:main",
            "badmaps=drawtools.compare.maps:main",
            "correlation=drawtools.compare.correlation:main",
            "chi2=drawtools.compare.chi2:main",
            "cbins=drawtools.compare.bins:main",
        ],
    },
)
