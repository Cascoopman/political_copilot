"""
This file is where your routes (endpoints) are defined. This file should only
contain logic related to the routes themselves (eg. parameter checking). Any
app logic should be moved to core.py.
"""

from app import core


class Example:
    """Includes all HTTP methods for Example"""

    @staticmethod
    def get(path_param, query_arg):
        """Example endpoint to get information."""
        return core.get_example(path_param, query_arg), 200

    @staticmethod
    def post(path_param, payload):
        """Example endpoint to post information."""
        return core.post_example(path_param, payload), 201
