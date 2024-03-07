#!/usr/bin/env python3

import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

def name_server():
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        r.set("ConnectChat", "127.0.0.1:xxxx")
        r.set("GroupChat", "127.0.0.1:xxxx")
        r.set("Discover", "xxxxxx:xxxx")
        r.set("InsultChannel", "127.0.0.1:xxxx")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    name_server()
