from flask import url_for
from application import BaseTestCase


class AuthTest(BaseTestCase):
    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get_200(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    def test_auth_login_template(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)
        self.assertTemplateUsed('login.html')

    def test_index_redirects(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }

        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('index'))
