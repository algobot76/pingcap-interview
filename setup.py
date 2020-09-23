from setuptools import setup

setup(
    name="pingcap-interview",
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'fuzz = packages.cli:fuzz',
            'seed = packages.cli:seed'
        ]
    }

)
