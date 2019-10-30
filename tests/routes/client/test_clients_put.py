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

        response = self.client.put(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 200)

    def test_response_success(self):
        self.login()

        expected_text_response = {
            "status": 200,
            "message": "Client updated",
            "code": "success",
            "data": {
                "id": "5945d7a6-306e-4f55-97e1-7a96de89d8d7",
                "name": "test luiza",
                "email": "test@luizalabs.com",
            },
        }

        response = self.client.put(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_content_type_success(self):
        self.login()

        response = self.client.put(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"name": "test luiza", "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertIn("application/json", response.content_type)

    def test_status_body_incorrect(self):
        self.login()

        response = self.client.put(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"name": None, "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 400)

    def test_response_body_incorrect(self):
        self.login()

        expected_text_response = {
            "status": 400,
            "message": "The body does not match the scheme",
            "code": "body_incorrect",
            "data": {"name": ["Field may not be null."]},
        }

        response = self.client.put(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"name": None, "email": "test@luizalabs.com"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)


if __name__ == "__main__":
    unittest.main()
