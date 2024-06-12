import redis 
import json 

rds = redis.StrictRedis(port=6379, db=0)


class Red:
    def set(cache_key, data):
        data = json.dumps(data)
        rds.set(cache_key, data) 
        
        return True 

    def get(cache_key):
        cached_data = rds.get(cache_key)
        
        if cached_data:
            cached_data = json.loads(cached_data) 
        
        return cached_data