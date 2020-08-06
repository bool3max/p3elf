# **p3elf**

A tiny python3 module for parsing ELF file metadata that I'm writing to familiarize myself with python binary IO as well as to gain more python experience.

Currently, it can: 

* parse the ELF file header

* parse program headers and section headers

* dump segments

* dump sections

## Installation

```sh
$ pip3 install -U p3elf
```

### Basic usage

```python

>>> import p3elf.reader
>>> elf = p3elf.reader.ELFReader('/bin/bash')
>>> elf.get_header()['EI_MACHINE']

'amd64'
```

## TODO
* cli tool
* docs
