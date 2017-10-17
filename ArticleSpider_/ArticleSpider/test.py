import redis

redis_cli = redis.StrictRedis()
redis_cli.incr("jobble_count")
