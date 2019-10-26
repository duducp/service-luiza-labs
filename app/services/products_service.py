import requests

import settings
from app.utils.requests import Requests


class ProductService:
    def __init__(self):
        self._config = settings.load_config()
        self._requests = Requests(expiration=30)

    def get_one(self, _id: str) -> requests:
        try:
            headers = {"Content-Type": "application/json"}

            r = self._requests.get(
                url=f"{self._config.SERVICE_PRODUCTS}/{_id}",
                headers=headers,
                timeout=10,
            )
            return r
        except requests.exceptions.Timeout:
            raise Exception("Request has timed out")
        except requests.exceptions.RequestException as e:
            raise e
        except Exception as e:
            raise e

    def get_all(self, page: int = 1) -> requests:
        try:
            headers = {"Content-Type": "application/json"}

            r = self._requests.get(
                url=f"{self._config.SERVICE_PRODUCTS}?page={page}",
                headers=headers,
                timeout=10,
            )
            return r
        except requests.exceptions.Timeout:
            raise Exception("Request has timed out")
        except requests.exceptions.RequestException as e:
            raise e
        except Exception as e:
            raise e
