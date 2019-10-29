import unittest

import requests_mock

from app.utils.requests import Requests


class RequestsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.r = Requests()

    def test_headers(self) -> None:
        header = self.r.headers
        self.assertEqual(
            header,
            {
                "User-Agent": "python-requests/2.22.0",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "*/*",
                "Connection": "keep-alive",
            },
        )

    @requests_mock.mock()
    def test_get_ok(self, m):
        m.register_uri(
            "GET", "http://localhost", json={"name": "doug_doug"}, status_code=200
        )
        response = self.r.get("http://localhost")
        self.assertDictEqual(response.json(), {"name": "doug_doug"})

    @requests_mock.mock()
    def test_post_ok(self, m):
        m.register_uri(
            "POST", "http://localhost", json={"name": "doug_doug"}, status_code=200
        )
        response = self.r.post("http://localhost")
        self.assertDictEqual(response.json(), {"name": "doug_doug"})

    @requests_mock.mock()
    def test_put_ok(self, m):
        m.register_uri(
            "PUT", "http://localhost", json={"name": "doug_doug"}, status_code=200
        )
        response = self.r.put("http://localhost")
        self.assertDictEqual(response.json(), {"name": "doug_doug"})

    @requests_mock.mock()
    def test_delete_ok(self, m):
        m.register_uri("DELETE", "http://localhost", json={}, status_code=200)
        response = self.r.delete("http://localhost")
        self.assertDictEqual(response.json(), {})

    @requests_mock.mock()
    def test_request_ok(self, m):
        m.register_uri(
            "GET", "http://localhost", json={"name": "doug_doug"}, status_code=200
        )
        response = self.r.request("GET", "http://localhost")
        self.assertDictEqual(response.json(), {"name": "doug_doug"})


if __name__ == "__main__":
    unittest.main()
