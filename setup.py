from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'fuzz = packages.cli:fuzz'
        ]
    }

)
