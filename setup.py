from setuptools import find_packages, setup

setup(
    name="pyEOCharging",
    packages=find_packages(include=["eocharging"]),
    version="0.0.2",
    description="EO Smart Charger Library",
    author="bfayers",
    license="GPLv3",
    install_requires=["requests>=2.25.1"],
)
