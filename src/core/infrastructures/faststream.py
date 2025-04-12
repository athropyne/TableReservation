from faststream.redis.fastapi import RedisBroker

from src.core import config

broker = RedisBroker(f"redis://{config.settings.REDIS_SOCKET}")


