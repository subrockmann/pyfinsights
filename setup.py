from setuptools import find_packages, setup

setup(
    name="pyfinsights",
    packages=find_packages(include=["pyfinsights"]),
    version="0.1.0",
    description="Python library for extracting financial insights from different sources.",
    author="subrockmann",
    install_requires=["yfinance"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)