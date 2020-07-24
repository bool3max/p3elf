def find_key(d, val):
    # find a dict key corresponding to the requested value (if there are more keys with the same value, the first matching one is returned)
    for k, v in d.items():
        if v == val:
            return k
    return None

class p3elfError(Exception):
    # all exception classes defined by p3elf inherit this exception class to make it easy for library consumers to catch all exceptions raised by p3elf
    pass

class InvalidFileFormat(p3elfError):
    def __init__(self, expected=None, got=None):
        self.expected = expected
        self.got = got
        if not expected or not got:
            self.message = "Expected different file format"
        else:
            self.message = f"Expected '{expected}', got '{got}'"
        super(p3elfError, self).__init__(self.message)

class NoSection(p3elfError):
    pass
