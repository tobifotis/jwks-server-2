import unittest
import json
from app import create_app
from app.db import initialize_db


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        initialize_db()

    def test_generate_keys(self):
        response = self.app.post('/generate-keys')
        self.assertEqual(response.status_code, 201)

    def test_auth_endpoint(self):
        self.app.post('/generate-keys')
        response = self.app.post('/auth', json={'username': 'test_user'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)

    def test_jwks_endpoint(self):
        self.app.post('/generate-keys')
        response = self.app.get('/.well-known/jwks.json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('keys', data)


if __name__ == '__main__':
    unittest.main()
