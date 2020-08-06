# build the package using setuptools

import setuptools, io
from p3elf import __version__ as version

with io.open("./README.md", "r") as f:
    ld = f.read()

args = {
    "name": "p3elf",
    "version": version,
    "author": "Bogdan Mitrović",
    "author_email": "bokisa.mitrovic2@gmail.com",
    "description": "A tiny python3 package for parsing ELF files",
    "long_description": ld,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/bool3max/p3elf/",
    "packages": setuptools.find_packages(),
    "classifiers": ["Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent"],
    "python_requires": ">=3.5"
}

print(setuptools.find_packages())

setuptools.setup(**args)
