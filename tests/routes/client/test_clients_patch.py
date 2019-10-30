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

        response = self.client.patch(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"email": "test@luizalabs.com"},
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
                "email": "admin@luizalabs.com",
            },
        }

        response = self.client.patch(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"name": "test luiza"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_content_type_success(self):
        self.login()

        response = self.client.patch(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            json={"name": "test luiza"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertIn("application/json", response.content_type)


if __name__ == "__main__":
    unittest.main()
