import unittest

from tests.base import BaseTestCase


class LoginTestCase(BaseTestCase):
    def login(self):
        response = self.client.post(
            "/auth/login",
            json={"email": "admin@luizalabs.com"},
            content_type="application/json",
        )

        self.refresh = ""
        if response.status_code == 201:
            data = response.json.get("data", {})
            self.refresh = data.get("refresh_token", "")

    def test_status_success(self):
        self.login()

        response = self.client.get(
            "/auth/refresh",
            headers={"authorization": self.refresh, "content-type": "application/json"},
        )
        self.assertEqual(response.status_code, 201)

    def test_content_type_success(self):
        self.login()

        response = self.client.get(
            "/auth/refresh",
            headers={"authorization": self.refresh, "content-type": "application/json"},
        )
        self.assertIn("application/json", response.content_type)

    def test_not_informed_authorization(self):
        response = self.client.get(
            "/auth/refresh", headers={"content-type": "application/json"}
        )
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
