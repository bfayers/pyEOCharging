from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="pyEOCharging",
    packages=find_packages(include=["eocharging"]),
    version="0.0.6",
    description="EO Smart Charger Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bfayers/pyEOCharging",
    project_urls={
        "Bug Tracker": "https://github.com/bfayers/pyEOCharging/issues",
    },
    author="bfayers",
    license="GPLv3",
    install_requires=["requests>=2.25.1"],
)
