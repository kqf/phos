from setuptools import setup, find_packages

setup(
    name="kinematics",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'generate=phasegen.main:main',
        ],
    },
)
