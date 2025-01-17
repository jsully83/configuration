from setuptools import setup, find_packages

setup(
    name="configuration",
    version="0.1.0",
    author="Jonathan Sullivan",
    author_email="sullivan.jona@northeastern.edu",
    description="simple configuration and logging using munch and loguru",
    packages=find_packages(),
    install_requires=[
        "munch",
        "pyyaml",
        "loguru" # List dependencies here
    ],
    python_requires=">=3.6",
)