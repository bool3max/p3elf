# **p3elf**

A tiny python3 module for parsing ELF file metadata that I'm writing to familiarize myself with python binary IO as well as to gain more python experience.

Currently, it can: 

    * parse the ELF file header

    * parse all program headers

    * dump segments

## TODO
* publish on pip for fun (familiarize myself with setuptools etc.)
* parse flag fields from the progheader and section headers into human-readable strings (just as `readelf` does)
* cli tool
