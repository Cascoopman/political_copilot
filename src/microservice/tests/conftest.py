"""
root conftest definition
"""

import pytest

from app.flask import create_app


@pytest.fixture
def client():
    """
    Construct the base test client based on the app factory
    """
    app = create_app().app
    app.config['TESTING'] = True

    with app.test_client() as test_client:
        yield test_client
