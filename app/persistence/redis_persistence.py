import json

from logzero import logger
from redis import StrictRedis

import settings
from app.utils.singleton import Singleton


class RedisPersistence(object):
    def __init__(self, db=0):
        self._config = settings.load_config()
        self._host = self._config.REDIS_HOST
        self._port = self._config.REDIS_PORT
        self._db = db
        self.conn = self.get_instance

    def __del__(self):
        self.close_connection()

    @property
    def connection_database(self) -> StrictRedis:
        return StrictRedis(
            host=self._host,
            port=self._port,
            db=self._db,
            charset="utf-8",
            decode_responses=True,
        )

    @property
    def get_instance(self):
        rw = Singleton()
        rw.conn = self.connection_database
        return rw.conn

    def close_connection(self):
        self.conn.close()

    def test_ping(self) -> bool:
        try:
            return self.conn.ping()
        except Exception as ex:
            logger.error(f"Error testing Redis ping. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def set_expires(self, key: str, value: str, expires_minutes: float) -> None:
        try:
            if not isinstance(value, str):
                value = json.dumps(value)

            expires = expires_minutes * 60

            self.conn.hset(name=key, key=key, value=value)
            self.conn.expire(name=key, time=expires)
        except Exception as ex:
            logger.error(
                f"Error saving value with expires in Redis. ERROR ---> {str(ex)}"
            )
            raise Exception(ex)

    def set(self, name: str, key: str, value: str) -> None:
        try:
            if not isinstance(value, str):
                value = json.dumps(value)

            self.conn.hset(name=name, key=key, value=value)
        except Exception as ex:
            logger.error(f"Error saving value in Redis. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def get(self, name: str, key: str) -> str:
        try:
            return self.conn.hget(name=name, key=key)
        except Exception as ex:
            logger.error(f"Error getting value in Redis. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def get_all(self, name: str) -> dict:
        try:
            return self.conn.hgetall(name=name)
        except Exception as ex:
            logger.error(f"Error getting all values in Redis. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def delete(self, name: str, key: str) -> None:
        try:
            self.conn.hdel(name, key)
        except Exception as ex:
            logger.error(f"Error deleting value in Redis. ERROR ---> {str(ex)}")
            raise Exception(ex)
