import json
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from logzero import logger

import settings
from app.persistence.redis_persistence import RedisPersistence


class JwtUtils:
    def __init__(self):
        self._private_key = self._get_private_key()
        self._public_key = self._get_public_key()
        self._now = datetime.now()
        self._config = settings.load_config()
        self._redis = RedisPersistence()

    def generate_access_and_refresh_token(self, client_id: str) -> dict:
        jti_access = str(uuid4())
        jti_refresh = str(uuid4())

        access_token = self.generate(
            client_id=str(client_id),
            expires_minutes=self._config.TOKEN_ACCESS_EXP_MINUTES,
            type="access_token",
            jti_access=jti_access,
            jti_refresh=jti_refresh,
        )

        self._redis.set_expires(
            key=jti_access,
            value=json.dumps({"valid": True, "token": access_token}),
            expires_minutes=self._config.TOKEN_ACCESS_EXP_MINUTES,
        )

        refresh_token = self.generate(
            client_id=str(client_id),
            expires_minutes=self._config.TOKEN_REFRESH_EXP_MINUTES,
            type="refresh_token",
            jti_access=jti_access,
            jti_refresh=jti_refresh,
        )

        self._redis.set_expires(
            key=jti_refresh,
            value=json.dumps({"valid": True, "token": refresh_token}),
            expires_minutes=self._config.TOKEN_REFRESH_EXP_MINUTES,
        )

        return {"access_token": access_token, "refresh_token": refresh_token}

    def generate(
        self,
        type: str,
        expires_minutes: int,
        client_id: str,
        jti_access: str = None,
        jti_refresh: str = None,
    ) -> str:
        try:
            exp = self._now + timedelta(minutes=expires_minutes)

            payload = {
                "iat": int(self._now.timestamp()),
                "exp": int(exp.timestamp()),
                "client_id": client_id,
                "jti_access": jti_access,
                "jti_refresh": jti_refresh,
                "iss": "auth_user",
                "type": type,
            }
            token = jwt.encode(
                payload=payload, key=self._private_key, algorithm="RS256"
            ).decode("utf-8")

            return token
        except jwt.DecodeError as e:
            raise Exception(f"Error decoding the token: {e}")
        except jwt.ExpiredSignature as e:
            raise Exception(f"The reported token has expired: {e}")
        except jwt.InvalidTokenError as e:
            raise Exception(f"The token entered is not valid: {e}")
        except Exception as e:
            raise Exception(f"Error generate token: {e}")

    def decode(self, token, verify=True):
        try:
            if verify:
                return jwt.decode(
                    jwt=token, key=self._public_key, verify=verify, algorithm=["RS256"]
                )
            else:
                return jwt.decode(jwt=token, verify=verify)
        except jwt.ExpiredSignature:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            logger.error("Error decodes signed token: {}".format(str(e)))
            raise Exception(e)

    def revoke(self, key: str, expires_minutes: int) -> bool:
        try:
            token = self._redis.get(key, key)
            if token:
                token = json.loads(token)
                token["valid"] = False
                self._redis.delete(key, key)
                self._redis.set_expires(
                    key=key, value=token, expires_minutes=expires_minutes
                )
            return True
        except Exception as e:
            logger.error("Erro ao revogar o token: {}".format(str(e)))
            return False

    def valid_token(self, token: str) -> dict:
        try:
            payload = self.decode(token=token)
            if not payload:
                return {}

            key = payload.get("jti_refresh")
            if payload.get("type") == "access_token":
                key = payload.get("jti_access")

            tokens_redis = self._redis.get(name=key, key=key)
            if not all([tokens_redis, json.loads(tokens_redis).get("valid")]):
                return {}

            return payload
        except Exception as e:
            logger.error("Erro ao validar o token: {}".format(str(e)))
            return {}

    @staticmethod
    def _get_private_key():
        pemfile = open("keys/private.pem", "r")
        private_key = pemfile.read()
        pemfile.close()
        return private_key

    @staticmethod
    def _get_public_key():
        pemfile = open("keys/public.pem", "r")
        public_key = pemfile.read()
        pemfile.close()
        return public_key
