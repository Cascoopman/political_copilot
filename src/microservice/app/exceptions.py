"""
Expand the basic Exception class with app specific exceptions
to be raised by the error handler.
"""


class ExampleNotFound(Exception):
    """Exception to raise when a Example is not found."""
