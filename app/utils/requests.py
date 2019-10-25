import requests
import requests_cache
from logzero import logger
from requests import Response


class Requests(object):
    def __init__(self, name="cache", expiration=None):
        requests_cache.install_cache(cache_name=name, expire_after=expiration)
        self._get_session()

    def __del__(self):
        self.session.close()
        delattr(self, "_session")

    def _get_session(self):
        self._session = requests.Session()

    @property
    def session(self):
        if hasattr(self, "_session"):
            self._get_session()

        return self._session

    @property
    def headers(self):
        return self.session.headers

    def request(self, method, url, **kwargs) -> Response:
        response = self.session.request(method=method, url=url, **kwargs)
        logger.info(f"{method} <{response.status_code}> [{url}]")
        return response

    def get(self, url, **kwargs) -> Response:
        response = self.session.get(url=url, **kwargs)
        logger.info(f"GET <{response.status_code}> [{url}]")
        return response

    def post(self, url, **kwargs) -> Response:
        response = self.session.post(url=url, **kwargs)
        logger.info(f"POST <{response.status_code}> [{url}]")
        return response

    def put(self, url, **kwargs) -> Response:
        response = self.session.put(url=url, **kwargs)
        logger.info(f"PUT <{response.status_code}> [{url}]")
        return response

    def delete(self, url, **kwargs) -> Response:
        response = self.session.delete(url=url, **kwargs)
        logger.info(f"DELETE <{response.status_code}> [{url}]")
        return response
