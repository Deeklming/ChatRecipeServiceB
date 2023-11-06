import redis
from os import getenv as cfg

def dbcache():
    try:
        r = redis.Redis(host=cfg("REDIS_HOST"), port=int(cfg("REDIS_PORT")), db=int(cfg("REDIS_DB0")), protocol=int(cfg("REDIS_PROTOCOL")))
    except Exception as e:
        print(f"redis connection failure!: {e}")
    return r

async def cache_test():
    cc = dbcache()
    cc.set("a", "test")
    print(cc.get("a"))
    cc.delete("a")
    print("[[dbcache test ok]]")
