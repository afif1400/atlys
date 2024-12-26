import redis
from app.config import Settings

class RedisCache:
    def __init__(self):
        settings = Settings()
        self.redis = redis.Redis(
              host=settings.REDIS_HOST,
              port=6379,
              password=settings.REDIS_PASSWORD,
              ssl=True
            )

    def get(self, key: str) -> str:
        return self.redis.get(key)

    def set(self, key: str, value: str, expire: int = 86400):
        self.redis.set(key, value, ex=expire)
