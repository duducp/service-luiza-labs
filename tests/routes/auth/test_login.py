import unittest

from tests.base import BaseTestCase


class LoginTestCase(BaseTestCase):
    def test_status_success(self):
        response = self.client.post(
            "/auth/login",
            json={"email": "admin@luizalabs.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_isinstance_response_success(self):
        response = self.client.post(
            "/auth/login",
            json={"email": "admin@luizalabs.com"},
            content_type="application/json",
        )
        self.assertIsInstance(response.json, dict)

    def test_content_type_success(self):
        response = self.client.post(
            "/auth/login",
            json={"email": "admin@luizalabs.com"},
            content_type="application/json",
        )
        self.assertIn("application/json", response.content_type)

    def test_credentials_error(self):
        response = self.client.post(
            "/auth/login",
            json={"email": "carlos@luizalabs.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_email_invalid(self):
        response = self.client.post(
            "/auth/login", json={"email": "sdfsdfsdf"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
