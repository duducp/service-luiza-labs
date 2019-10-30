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
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 201)

    def test_isinstance_response_success(self):
        self.login()

        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertIsInstance(response.json, dict)

    def test_content_type_success(self):
        self.login()

        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertIn("application/json", response.content_type)

    def test_status_no_body(self):
        self.login()

        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
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
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_status_product_not_found(self):
        self.login()

        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            content_type="application/json",
            json={"product_id": "bd3fb6a7-0f02-4369-8427-7e52dff9598e"},
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 404)

    def test_response_product_not_found(self):
        self.login()

        expected_text_response = {
            "status": 404,
            "message": "The product entered was not found",
            "code": "product_not_found",
            "data": None,
        }

        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            content_type="application/json",
            json={"product_id": "bd3fb6a7-0f02-4369-8427-7e52dff9598e"},
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_status_duplicated(self):
        self.login()

        self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )

        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.status_code, 409)

    def test_response_duplicated(self):
        self.login()

        expected_text_response = {
            "status": 409,
            "message": "Key (client_id, product_id)=(5945d7a6-306e-4f55-97e1-7a96de89d8d7, 1bf0f365-fbdd-4e21-9786-da459d78dd1f) already exists.",
            "code": "duplicated_key",
            "data": {"constraint_name": ["favorites_client_id_product_id_key"]},
        }

        self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )

        response = self.client.post(
            "/clients/5945d7a6-306e-4f55-97e1-7a96de89d8d7/favorites",
            json={"product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"},
            content_type="application/json",
            headers={"authorization": self.authorization},
        )
        self.assertEqual(response.json, expected_text_response)


if __name__ == "__main__":
    unittest.main()
