# db_tool/cache.py
import redis
import pickle

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def set(self, key, value):
        self.client.set(key, pickle.dumps(value))

    def get(self, key):
        value = self.client.get(key)
        return pickle.loads(value) if value else None

    def delete(self, key):
        self.client.delete(key)

