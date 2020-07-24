import io
from pathlib import Path, PurePath

from . import consts
from .misc import *

class ELFBase:
    """ Base class representing a single ELF file. Initialzing an instance of it sets up the path, opens the file for reading, extracts basic byteclass-independant information (endianness, byteclass).
    """

    @classmethod
    def is_elf_file(cls, reader):
        # reader must be open in binary mode
        prev = reader.tell()
        reader.seek(1) 
        ret = reader.read(3) == b"ELF"
        reader.seek(prev, 0)

        return ret

    def __init__(self, file_path):
        # 1. establish a public path to the elf file on the filesystem
        # 2. open the file for reading
        # 3. check if the file is an actual ELF file (via the magic number in the header), and if not, raise an exception and close the _reader
        # 4. establish whether it's a 32bit or 64bit executable
        # delegate all other operations (parsing the rest of the header, for example) to subclasses

        self.path = Path(file_path)
        self._reader = io.open(self.path, 'rb')

        if not ELFBase.is_elf_file(self._reader):
            raise InvalidFileFormat()

        self._reader.seek(consts.HEADER_FIELDS_DESC['EI_CLASS'][0][0]) # offset is same on 32bit and 64bit

        self.byteclass  = 32 if int.from_bytes(self._reader.read(1), 'little') == 1 else 64
        # previous read coincidentally seeked us to the next byte
        self.endianness = 'little' if int.from_bytes(self._reader.read(1), 'little') == 1 else 'big'

    def __del__(self):
        # close the open fd when the object is deleted
        self._reader.close()

class ELFReader(ELFBase):
    header_tuple_fields = ['EI_OSABI', 'EI_MACHINE', 'EI_OBJTYPE'] # header fields that are returned as tuples because they also have a string representation (i.e. EI_MACHINE, where 0x3e corresponds to 'amd64')
    progheader_tuple_fileds = ['P_TYPE']

    def get_header_field(self, field):
        """ Parse a single entry out of the program header and return its value as an integer """
        self._reader.seek(consts.HEADER_FIELDS_DESC[field][0][0] if self.byteclass == 32 else consts.HEADER_FIELDS_DESC[field][0][1])
        num_val = int.from_bytes(self._reader.read(consts.HEADER_FIELDS_DESC[field][1][0] if self.byteclass == 32 else consts.HEADER_FIELDS_DESC[field][1][1]), self.endianness)

        # modules are not subscriptable so I cannot automatically query the appropriate dictionary from "consts" (i.e. consts['EI_OSABI']), unless I import them into this namespace, which I don't want to do
        # so I have to test for each tuple-returning field individually
        if field == 'EI_OSABI':
             return num_val, find_key(consts.EI_OSABI, num_val)
        elif field == 'EI_MACHINE':
             return num_val, find_key(consts.EI_MACHINE, num_val)
        elif field == 'EI_OBJTYPE':
             return num_val, find_key(consts.EI_OBJTYPE, num_val)
        else:
            return num_val

    def get_header(self):
        """ Parse the entirety of the ELF header and return a dictionary with all the appropriate fields. 
            The byteclass and the endianness are saved as attributes of the class instance object once it is initialized, but are also provided in the dict returned by this method
        """
        return {f: self.get_header_field(f) for f in consts.HEADER_FIELDS_DESC}
    def get_progheader_field(self, field, index=0):
        # fetch a specific field from the program header - if no program headers exist at the specified index, raise an appropriate exception
        num_pheaders = self.get_header_field('EI_PHNUM') # the total number of program headers in the file
        phsize = self.get_header_field('EI_PHENTSIZE') # the size of each program header

        if num_pheaders == 0 or (index > (num_pheaders - 1) or index < 0):
            raise NoSection(f"No program header found at index {index}")

        if (field == 'P_FLAGS' and self.byteclass == 32) or (field == 'P_FLAGS1' and self.byteclass == 64):
            # P_FLAGS doesn't exist on 32bit ELF files and P_FLAGS1 doesn't exist on 64bit ones
            return None

        self._reader.seek(self.get_header_field('EI_PHOFF') + (index * phsize)) # seek reader to start of program header
        self._reader.seek(consts.PROGHEADER_FIELDS_DESC[field][0][0] if self.byteclass == 32 else consts.PROGHEADER_FIELDS_DESC[field][0][1], 1) # seek to offset of requested field
        num_val =  int.from_bytes(self._reader.read(consts.PROGHEADER_FIELDS_DESC[field][1][0] if self.byteclass == 32 else consts.PROGHEADER_FIELDS_DESC[field][1][1]), self.endianness)

        if field == "P_TYPE":
            return num_val, find_key(consts.P_TYPE ,num_val)

        return num_val
    def get_progheader(self, index=0):
        return {f: self.get_progheader_field(f, index) for f in consts.PROGHEADER_FIELDS_DESC}

    def get_sectionheader_field(self, field):
        # fetch a specific field from the section header - if no section header exist in the ELF file, an appropriate exception is raised
        if self.get_header_field('EI_SHNUM') == 0:
            raise NoSection(f"Number of section headers in file: 0")
        # seek reader to the start of the section header table
        shoff = self.get_header_field('EI_SHOFF')
        self._reader.seek(shoff)


