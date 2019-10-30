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

        response = self.client.get(
            "/clients",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_response_success(self):
        self.login()

        expected_text_response = {
            "status": 200,
            "message": "Clients found successfully",
            "code": "success",
            "data": {
                "results": [
                    {
                        "email": "admin@luizalabs.com",
                        "name": "admin",
                        "id": "5945d7a6-306e-4f55-97e1-7a96de89d8d7",
                    }
                ],
                "page": 1,
                "size": 10,
                "total_items": 1,
                "total_pages": 1,
            },
        }

        response = self.client.get(
            "/clients",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertEqual(response.json, expected_text_response)

    def test_content_type_success(self):
        self.login()

        response = self.client.get(
            "/clients",
            headers={
                "authorization": self.authorization,
                "content-type": "application/json",
            },
        )
        self.assertIn("application/json", response.content_type)

    def test_status_token_not_informed(self):
        response = self.client.get(
            "/clients",
            headers={"authorization": "", "content-type": "application/json"},
        )
        self.assertEqual(response.status_code, 400)

    def test_response_token_not_informed(self):
        expected_text_response = {
            "status": 400,
            "message": "The token not entered in header",
            "code": "token_not_informed",
            "data": None,
        }

        response = self.client.get(
            "/clients",
            headers={"authorization": "", "content-type": "application/json"},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_content_type_token_not_informed(self):
        response = self.client.get(
            "/clients",
            headers={"authorization": "", "content-type": "application/json"},
        )
        self.assertIn("application/json", response.content_type)

    def test_status_not_authorized(self):
        response = self.client.get(
            "/clients",
            headers={"authorization": "sdsasad", "content-type": "application/json"},
        )
        self.assertEqual(response.status_code, 401)

    def test_response_not_authorized(self):
        expected_text_response = {
            "status": 401,
            "message": "The token entered is not valid",
            "code": "token_invalid",
            "data": None,
        }

        response = self.client.get(
            "/clients",
            headers={"authorization": "sadasdasd", "content-type": "application/json"},
        )
        self.assertEqual(response.json, expected_text_response)

    def test_content_type_not_authorized(self):
        response = self.client.get(
            "/clients",
            headers={"authorization": "sadasdasd", "content-type": "application/json"},
        )
        self.assertIn("application/json", response.content_type)


if __name__ == "__main__":
    unittest.main()
