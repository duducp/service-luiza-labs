from datetime import datetime

from logzero import logger

import settings
from app import db
from app.persistence.redis_persistence import RedisPersistence


class HealthController:
    def __init__(self):
        self._config = settings.load_config()
        self._redis = RedisPersistence()

    def verify(self):
        try:
            self._ping_redis()
            self._ping_database()

            data = {
                "environment": self._config.ENVIRONMENT,
                "datetime": datetime.now().isoformat(),
            }

            return data
        except Exception as e:
            raise Exception(e)

    def _ping_redis(self):
        try:
            return self._redis.test_ping()
        except Exception as e:
            logger.error(f"Failed to connect with Redis: {str(e)}")
            raise Exception("Failed to connect with Redis")

    @staticmethod
    def _ping_database() -> str:
        try:
            results = db.engine.execute("SELECT NOW()")
            for _result in results:
                return _result[0].isoformat()
        except Exception as e:
            logger.error(f"Failed to check sql alchemy: {str(e)}")
            raise Exception(f"Failed to check database")
        finally:
            db.session.close()
