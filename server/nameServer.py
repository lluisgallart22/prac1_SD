#!/usr/bin/env python3

import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

def name_server(tipus, ipport):
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        r.set(tipus, ipport)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    tipus = input()
    ipport = input()
    name_server(tipus, ipport)
