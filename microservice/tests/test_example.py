"""
All tests related to testing Example
the tests use an testing app that is client defined in the conftest.py
"""


class TestExample:  # nosec
    """Example integration test stubs"""

    @staticmethod
    def test_get_example(client):
        """Test case for get_example
        Example endpoint to get information.
        """
        query_string = [
            ('query_arg', 'query_arg_example'),
        ]

        response = client.open(
            '/example/{path_param}'.format(path_param='path_param_example'),
            method='GET',
            content_type='application/json',
            query_string=query_string,)
        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'success'

    @staticmethod
    def test_post_example(client):
        """Test case for post_example
        Example endpoint to post information.
        """
        data = {'id': Undefined, 'data': Undefined}

        response = client.open(
            '/example/{path_param}'.format(path_param='path_param_example'),
            method='POST',
            content_type='application/json', data=data
        )
        assert response.status_code == 201
        assert response.data.decode('utf-8') == 'OK'
