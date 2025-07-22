from setuptools import setup, find_packages

setup(
    name="mygit",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer>=0.16.0",
        "shellingham>=1.3.0",
    ],
    entry_points={
        'console_scripts': [
            'mygit = mygit.cli:main',
        ],
    },
)
