from flask import current_app, url_for
from application import BaseTestCase


class MainTest(BaseTestCase):
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello'))

    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)

    def test_hello_post(self):
        response = self.client.post(
            url_for('hello'), data={}
        )

        self.assertTrue(response.status_code, 405)