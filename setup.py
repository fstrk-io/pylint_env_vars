import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pylint_env_vars',
    version='0.1',
    description='pylint_env_vars',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kurtgn/pylint_env_vars',
    author='Mikhail Novikov',
    author_email='mikhail.g.novikov@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
)
