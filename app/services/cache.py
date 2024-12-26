from app.services.redis import RedisCache

class CacheService:
    def __init__(self):
        # the cache service uses redis can be replaced with any other cache service
        self.redis = RedisCache()

    def get(self, key: str) -> str:
        return self.redis.get(key)

    def set(self, key: str, value: str, expire: int = 86400):
        self.redis.set(key, value, expire=expire)
