import codecs
import os
import re
from setuptools import find_packages, setup

DESCRIPTION = "A python library that implements a thrift parser into Django to use it's models and controllers to " \
              "implement RPC/HTTP services. "

main_package = "grppy"

EXCLUDE_PACKAGES = [
    "*.tests",
    "*.tests.*",
    "tests.*",
    "tests",
]


def read(*parts):
    with codecs.open(os.path.join(cwd, *parts), 'r') as fp:
        return fp.read()


def find_info(*file_paths, info='version'):
    """ Get __{info}__ from a list of file paths
    """
    version_file = read(*file_paths)
    version_match = re.search(f"^__{info}__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

cwd = os.path.abspath(os.path.dirname(__file__))

version = find_info(main_package, "__init__.py", info='version')

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name=find_info(main_package, "__init__.py", info='title'),
    version=version,
    packages=find_packages(exclude=EXCLUDE_PACKAGES),
    include_package_data=True,
    license='Apache 2.0 License',
    description=DESCRIPTION,
    long_description=README,
    url='https://github.com/dstarner/grppy',
    author=find_info(main_package, "__init__.py", info='author'),
    author_email=find_info(main_package, "__init__.py", info='email'),
    install_requires=[
        'lark-parser'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
