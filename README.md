# **p3elf**

A tiny python3 module for parsing ELF file metadata that I'm writing to familiarize myself with python binary IO as well as to gain more python experience.

Currently has the ability to read the File Header as well as the Program Headers.

## TODO
* add ability to parse various section headers
* cli tool
* publish on pip for fun (familiarize myself with setuptools etc.)
* parse flag fields from the progheader into human-readable strings (just as `readelf` does)
