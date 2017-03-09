# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

from exceptions import *

RUNNING_REPL = False

def enable_repl():
    global RUNNING_REPL
    RUNNING_REPL = True

def complain_and_die(message):
    raise KimiParsingError(message)

def assert_or_complain(assertion, message):
    try:
        assert assertion
    except AssertionError:
        complain_and_die(message)


def throw_error(err_type, message):
    error_type = err_type.title()
    if error_type not in ["Name", "Syntax", "Type"]:
        error_type = "Unknown"
    error = error_type + "Error"
    exception = eval("Kimi" + error_type + "Error")(error + " : " + message)
    raise exception

def print_or_raise_exception(exception):
    if RUNNING_REPL:
        print(exception)
    else:
        raise exception

def assert_or_throw(assertion, err_type, message):
    try:
        assert assertion
    except AssertionError:
        throw_error(err_type, message)
