from flask_testing import TestCase

from main import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app
