#!/usr/bin/env python3

import redis
import argparse

r = redis.Redis(host='localhost', port=6379)

#Pels clients db = 0, pels xats grupals db = 1

def set_chat_connection(ip, port, nomConnexio, db):
    r.hset(f'nom:{nomConnexio}', mapping={
        'ip': ip,
        'port': port,
        'db': db
    })

def get_chat_connection(nomConnexio):
    parametres = r.hgetall(f'nom:{nomConnexio}')
    if parametres:
        return{
            'ip': parametres[b'ip'].decode('utf-8'),
            'port': int(parametres[b'port']),
            'db': int(parametres[b'db'])
        }
    else:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Paràmetres necessàris pel set o get")
    subparser = parser.add_subparsers(dest='command')

    set_parser = subparser.add_parser('set', help='Paràmetres necessaris pel set')
    set_parser.add_argument('ip', type=str, help='Adreça IP del nou client/xat grupal')
    set_parser.add_argument('port', type=int, help='Port del nou client/xat')
    set_parser.add_argument('nomConnexio', type=str, help='Nom del client/xat grupal')
    set_parser.add_argument('db', type=int, help='Numero de la base de dades segons si és un client o un xat grupal')

    get_parser = subparser.add_parser('get', help='Paràmetres necessàris pel get')
    get_parser.add_argument('nomConnexio', type=str, help='Nom del xat grupal o del client')

    args = parser.parse_args()

    if args.command == 'set':
        set_chat_connection(args.ip, args.port, args.nomConnexio, args.db)
    elif args.command == 'get':
        resultat = get_chat_connection(args.nomConnexio)
        if resultat:
            print(f"Connection for {args.nomConnexio}: IP={resultat['ip']}, Port={resultat['port']}, DB={resultat['db']}")
        else:
            print(f"No connection found for {args.nomConnexio}.")
