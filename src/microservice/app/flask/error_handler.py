"""
Error handlers are responsible for converting any python exceptions into
Flask error codes. This enables the use of native Python exceptions for
handling errors in the 'Python part' of the code, while they will still be
presented according to Flask standards in the API.
"""

from flask import jsonify

from app import exceptions


def handle_not_implemented(_):
    """Handle not implemented errors."""
    response = jsonify({'message': 'Not Implemented'})
    response.status_code = 501
    return response


def handle_not_found(error):
    """Handle not found errors."""
    response = jsonify({'message': str(error)})
    response.status_code = 404
    return response


def register_error_handlers(app):
    """Add error handlers to the app."""
    app.add_error_handler(NotImplementedError, handle_not_implemented)
    app.add_error_handler(exceptions.ExampleNotFound, handle_not_found)
