import unittest

from tests.base import BaseTestCase


class ClientTestCase(BaseTestCase):
    def test_status_success(self):

        response = self.client.post(
            "/auth/register",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_isinstance_response_success(self):
        response = self.client.post(
            "/auth/register",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
        )
        self.assertIsInstance(response.json, dict)

    def test_content_type_success(self):
        response = self.client.post(
            "/auth/register",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
        )
        self.assertIn("application/json", response.content_type)

    def test_status_no_body(self):
        response = self.client.post("/auth/register", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_response_no_body(self):
        expected_text_response = {
            "status": 400,
            "message": "The request body must be informed",
            "code": "body_not_informed",
            "data": None,
        }

        response = self.client.post("/auth/register", content_type="application/json")
        self.assertEqual(response.json, expected_text_response)

    def test_status_email_invalid(self):
        response = self.client.post(
            "/auth/register",
            content_type="application/json",
            json={"name": "test luiza", "email": "test@luizalabs"},
        )
        self.assertEqual(response.status_code, 400)

    def test_response_email_invalid(self):
        expected_text_response = {
            "status": 400,
            "message": "The body does not match the scheme",
            "code": "body_incorrect",
            "data": {"email": ["Not a valid email address."]},
        }

        response = self.client.post(
            "/auth/register",
            content_type="application/json",
            json={"name": "test luiza", "email": "test@luizalabs"},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_status_duplicated(self):
        self.client.post(
            "/auth/register",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
        )

        response = self.client.post(
            "/auth/register",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 409)

    def test_response_duplicated(self):
        expected_text_response = {
            "status": 409,
            "message": "Key (email)=(test@luizalabs.com) already exists.",
            "code": "duplicated_key",
            "data": {"constraint_name": ["clients_email_key"]},
        }

        self.client.post(
            "/auth/register",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
        )

        response = self.client.post(
            "/auth/register",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
        )
        self.assertEqual(response.json, expected_text_response)


if __name__ == "__main__":
    unittest.main()
