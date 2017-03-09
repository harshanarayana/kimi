"""
Kimi Specific Custom Exceptions to use for making the Kimi REPL more
interactive post Error.

Currently, they die if there is an exception. This can be prevented if the kimi
Raises exceptions and informs the users about the issue and then lets them
continue with their work as if nothing ever happened. (WEll, I said it)
"""


class KimiNameError(Exception):
    """
    This is a replacement for Python's NameError.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class KimiSyntaxError(Exception):
    """
    Replacement for Python's SyntaxError
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class KimiTypeError(Exception):
    """
    Replacement for Python's TypeError
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class KimiParsingError(Exception):
    """
    Parser Error in case of running .kimi scripts.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class KimiUnknownException(Exception):
    """
    When the Exception Type is not any that is defined above.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

