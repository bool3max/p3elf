# **p3elf**

A tiny python3 module for parsing ELF file metadata that I'm writing to familiarize myself with python binary IO as well as to gain more python experience.

Currently, it can: 

* parse the ELF file header

* parse program headers and section headers

* dump segments

* dump sections

## Installation

1. From `PyPI`

```sh
$ pip3 install -U p3elf
```

2. From source

* Clone this repository: 

    + `$ git clone https://github.com/bool3max/p3elf`

* Install using `setup.py` as usual

    + `$ python3 p3elf/setup.py install`

### Basic usage

```python

>>> import p3elf.reader
>>> elf = p3elf.reader.ELFReader('/bin/bash')
>>> elf.get_header()['EI_MACHINE']

'amd64'

>>> elf.sections()

['', '.interp', '.note.gnu.build-id', '.note.ABI-tag', '.gnu.hash', '.dynsym', '.dynstr', ...]
```

## TODO
* cli tool
* docs
