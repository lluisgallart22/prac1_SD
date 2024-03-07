#!/usr/bin/env python3

import redis
import sys

redis_host = "localhost"
redis_port = 6379
redis_password = ""

option = sys.argv[1]

def get_info():
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        info = r.get(option)
        return info
    except Exception as e:
        print(e)
        return 0

if __name__ == '__main__':
    print(get_info())
