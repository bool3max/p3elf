# --- constant definitions used throughout the library- -- 

# the size of the ELF HEADER, depends on the byte class
ELF_HEADER_32_LEN = 52
ELF_HEADER_64_LEN = 64

# describes offset, size, and field name of every field in the ELF file header
HEADER_FIELDS_DESC = {
    'EI_MAG': ((0x0, 0x0), (4, 4)),
    'EI_CLASS': ((0x04, 0x04), (1, 1)), # byte class, i.e. 32bit or 64bit
    'EI_DATA': ((0x05, 0x05), (1, 1)), # endianness, 1: little, 2:big,
    'EI_VERSION': ((0x06, 0x06), (1, 1)), # always 1
    'EI_OSABI': ((0x07, 0x07), (1, 1)), # underlying OS ABI, usually 0 regardless of actual platform,
    'EI_ABIVERSION': ((0x08, 0x08), (1, 1)), # ABI version, interpretation depends on platform,
    'EI_PAD': ((0x09, 0x09), (7, 7)), # unused, filled with 0s,
    'EI_OBJTYPE': ((0x10, 0x10), (2, 2)), # object file type,
    'EI_MACHINE': ((0x12, 0x12), (2, 2)), # target ISA,
    'EI_VERSION1': ((0x14, 0x14), (4, 4)), # version of ELF, currently always 1,
    'EI_ENTRY_ADDR': ((0x18, 0x18), (4, 8)), # address of the entry point of execution,
    'EI_PHOFF': ((0x1c, 0x20), (4, 8)), # pointer to start of the program header table
    'EI_SHOFF': ((0x20, 0x28), (4, 8)), # pointer to start of the section header table,
    'EI_FLAGS': ((0x24, 0x30), (4, 4)), # interpretation depends on the target arch,
    'EI_EHSIZE': ((0x28, 0x34), (2, 2)), # size of this header (ELF file header -- known in advance but provided for ease of use),
    'EI_PHENTSIZE': ((0x2a, 0x36), (2, 2)), # size of each program header,
    'EI_PHNUM': ((0x2c, 0x38), (2, 2)), # number of entries in the program header table,
    'EI_SHENTSIZE': ((0x2e, 0x3a), (2, 2)), # size of each section header,
    'EI_SHNUM': ((0x30, 0x3c), (2, 2)), # number of section headers,
    'EI_SHSTRNDX': ((0x32, 0x3e), (2, 2)) # index of the section header table entry that contains the section names
}

# describes offset, size, and field name of every field in the ELF program header
PROGHEADER_FIELDS_DESC = {
    'P_TYPE': ((0x0, 0x0), (4, 4)), # type of segment that this program header complements
    'P_FLAGS': ((None, 0x4), (None, 4)), 
    'P_OFFSET': ((0x04, 0x08), (4, 8)), # offset to the segment that this particular program header describes
    'P_VADDR': ((0x08, 0x10), (4, 8)),
    'P_ADDR': ((0x0c, 0x18), (4, 8)), # the size of the segment that this particular program header describes
    'P_FILESZ': ((0x10, 0x20), (4, 8)),
    'P_MEMSZ': ((0x14, 0x28), (4, 8)),
    'P_FLAGS1': ((0x18, None), (4, None)),
    'P_ALIGN': ((0x1c, 0x30), (4, 8))
}

P_TYPE = {
    'PT_NULL': 0x0,
    'PT_LOAD': 0x1,
    'PT_DYNAMIC': 0x2,
    'PT_INTERP': 0x3,
    'PT_NOTE': 0x4,
    'PT_SHLIB': 0x5,
    'PT_PHDR': 0x6,
    'PT_TLS': 0x7,
    'PT_LOOS': 0x60000000,
    'PT_HIOS': 0x6FFFFFFF,
    'PT_LOPROC': 0x70000000,
    'PT_HIPROC': 0x7FFFFFFF
}

# underlying OS ABI
EI_OSABI = {
    'system_v'      : 0x0,
    'hp_ux'         : 0x1,
    'netbsd'        : 0x2,
    'linux'         : 0x3,
    'gnu_hurd'      : 0x4,
    'solaris'       : 0x6,
    'aix'           : 0x7,
    'irix'          : 0x8,
    'freebsd'       : 0x9,
    'tru64'         : 0x0a,
    'novell_modesto': 0x0b,
    'openbsd'       : 0x0c,
    'openvms'       : 0x0d,
    'nonstop_kernel': 0x0e,
    'aros'          : 0x0f,
    'fenix_os'      : 0x10,
    'cloudabi'      : 0x11,
    'stratus_technologies_openvos': 0x12
}

# object file type (no idea what this means)
EI_OBJTYPE = {
    'ET_NONE'       : 0x0,
    'ET_REL'        : 0x1,
    'ET_EXEC'       : 0x2,
    'ET_DYN'        : 0x3,
    'ET_CORE'       : 0x4,
    'ET_LOOS'       : 0xfe00,
    'ET_HIOS'       : 0xfeff,
    'ET_LOPROC'     : 0xff00,
    'ET_HIPROC'     : 0xffff
}

# target ISA (has lots of values, will only include x86, amd64, various arms, and powerpc)

EI_MACHINE = {
    'x86'    : 0x03,
    'amd64'  : 0x3e,
    'IA_64'  : 0x32,
    'RISC_V' : 0xF3,
    'ARM'    : 0x28,
    'Aarch64': 0xb7,
    'PowerPC': 0x14,
    'PowerPC64': 0x15
}

SECTHEADER_FIELDS_DESC = {
    'SH_NAME': ((0x0, 0x0), (4, 4)), # an offset to a string in the .shstrtab section that describes the name of this particular section
    'SH_TYPE': ((0x04, 0x04), (4, 4)),
    'SH_FLAGS': ((0x08, 0x08), (4, 8)),
    'SH_ADDR': ((0x0c, 0x10), (4, 8)),
    'SH_OFFSET': ((0x10, 0x18), (4, 8)),
    'SH_SIZE': ((0x14, 0x20), (4, 8)),
    'SH_LINK': ((0x18, 0x28), (4, 4)),
    'SH_INFO': ((0x1c, 0x2c), (4, 4)),
    'SH_ADDRALIGN': ((0x20, 0x30), (4, 8)),
    'SH_ENTSIZE': ((0x24, 0x38), (4, 8))
}

SH_TYPE = {
    'SHT_NULL': 0x0,
    'SHT_PROGBITS': 0x1,
    'SHT_SYMTAB': 0x2,
    'SHT_STRTAB': 0x3,
    'SHT_RELA': 0x4,
    'SHT_HAS': 0x5,
    'SHT_DYNAMIC': 0x6,
    'SHT_NOTE': 0x7,
    'SHT_NOBITS': 0x8,
    'SHT_REL': 0x9,
    'SHT_SHLIB': 0x0a,
    'SHT_DYNSYM': 0x0b,
    'SHT_INIT_ARRAY': 0x0e,
    'SHT_FINI_ARRAY': 0x0f,
    'SHT_PREINIT_ARRAY': 0x10,
    'SHT_GROUP': 0x11,
    'SHT_SYMTAB_SHNDX': 0x12,
    'SHT_NUM': 0x13,
    'SHT_LOOS': 0x60000000
}

SH_FLAGS = {
    'WRITE': 0x1,
    'ALLOC': 0x2,
    'EXECINSTR': 0x4,
    'MERGE': 0x10,
    'STRINGS': 0x20,
    'INFO_LINK': 0x40,
    'LINK_ORDER': 0x80,
    'OS_NONCONFORMING': 0x100,
    'GROUP': 0x200,
    'TLS': 0x400,
    'MASKOS': 0xff00000,
    'MASKPROC': 0xf000000,
    'ORDERED': 0x4000000,
    'EXCLUDE': 0x8000000
}
