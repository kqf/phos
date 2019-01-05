from setuptools import setup, find_packages

setup(
    name="trigger-qa",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "triggerqa=trigger.main:main",
        ],
    }
)
