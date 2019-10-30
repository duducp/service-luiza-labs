import unittest

from tests.base import BaseTestCase


class ClientTestCase(BaseTestCase):
    def login(self):
        response = self.client.post(
            "/auth/login",
            json={"email": "admin@luizalabs.com"},
            content_type="application/json",
        )

        self.authorization = ""
        if response.status_code == 201:
            data = response.json.get("data", {})
            self.authorization = data.get("access_token", "")

    def test_status_success(self):
        self.login()

        response = self.client.post(
            "/clients",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 201)

    def test_isinstance_response_success(self):
        self.login()

        response = self.client.post(
            "/clients",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertIsInstance(response.json, dict)

    def test_content_type_success(self):
        self.login()

        response = self.client.post(
            "/clients",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertIn("application/json", response.content_type)

    def test_status_no_body(self):
        self.login()

        response = self.client.post(
            "/clients",
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 400)

    def test_response_no_body(self):
        self.login()

        expected_text_response = {
            "status": 400,
            "message": "The request body must be informed",
            "code": "body_not_informed",
            "data": None,
        }

        response = self.client.post(
            "/clients",
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_status_email_invalid(self):
        self.login()

        response = self.client.post(
            "/clients",
            content_type="application/json",
            json={"name": "test luiza", "email": "test@luizalabs"},
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 400)

    def test_response_email_invalid(self):
        self.login()

        expected_text_response = {
            "status": 400,
            "message": "The body does not match the scheme",
            "code": "body_incorrect",
            "data": {"email": ["Not a valid email address."]},
        }

        response = self.client.post(
            "/clients",
            content_type="application/json",
            json={"name": "test luiza", "email": "test@luizalabs"},
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_status_duplicated(self):
        self.login()

        self.client.post(
            "/clients",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )

        response = self.client.post(
            "/clients",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 409)

    def test_response_duplicated(self):
        self.login()

        expected_text_response = {
            "status": 409,
            "message": "Key (email)=(test@luizalabs.com) already exists.",
            "code": "duplicated_key",
            "data": {"constraint_name": ["clients_email_key"]},
        }

        self.client.post(
            "/clients",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )

        response = self.client.post(
            "/clients",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)


if __name__ == "__main__":
    unittest.main()
