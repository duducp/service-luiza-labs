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

        response = self.client.delete(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertEqual(response.status_code, 204)

    def test_content_type_success(self):
        self.login()

        response = self.client.delete(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertIn("application/json", response.content_type)


if __name__ == "__main__":
    unittest.main()
