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

    def add_favorite(self):
        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.favorite_id = ""
        if response.status_code == 201:
            self.favorite_id = response.json.get("data", {}).get("id", "")

    def test_status_success(self):
        self.login()
        self.add_favorite()

        response = self.client.delete(
            f"/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites/{self.favorite_id}",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertEqual(response.status_code, 204)

    def test_content_type_success(self):
        self.login()
        self.add_favorite()

        response = self.client.delete(
            f"/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites/{self.favorite_id}",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertIn("application/json", response.content_type)

    def test_status_notfound(self):
        self.login()

        response = self.client.delete(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_response_notfound(self):
        self.login()

        expected_text_response = {
            "status": 404,
            "message": "Favorite ID you entered could not be found",
            "code": "favorite_not_found",
            "data": None,
        }

        response = self.client.delete(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites/5945d7a6-306e-4f55-97e1-7a96de89d8d7",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertEqual(response.json, expected_text_response)


if __name__ == "__main__":
    unittest.main()
