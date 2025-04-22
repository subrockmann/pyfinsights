from setuptools import find_packages, setup

setup(
    name="pyfinsights",
    packages=find_packages(include=["pyfinsights"]),
    version="0.1.5",
    description="Python library for extracting financial insights from different sources.",
    author="subrockmann",
    install_requires=["yfinance", "pandas", "ibapi"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)