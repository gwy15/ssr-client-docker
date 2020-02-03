#!/usr/bin/env python3
import base64
from urllib.parse import parse_qs
import argparse
import json

DEFAULT_CONFIG = {
    'local_address': '0.0.0.0',
    'local_port': 1080,
    'timeout': 30,
    'dns_ipv6': False
}


def decode_params(s):
    if len(s) % 4 != 0:
        s += '=' * (4 - len(s) % 4)
    return base64.decodebytes(s.encode('utf8')).decode('utf8')


def parse_url(s):
    if s.startswith('ssr://'):
        s = s[6:]
    decoded = decode_params(s)
    url, _, params = decoded.partition('/?')

    ip, port, protocol, method, obfs, pswd = url.split(':')

    parsed_params = parse_qs(params)

    result = {
        'server': ip, 'server_port': int(port),
        'password': decode_params(pswd), 'method': method,
        'protocol': protocol, 'obfs': obfs,
    }
    if 'obfsparam' in parsed_params:
        result['obfs_param'] = decode_params(
            parsed_params['obfsparam'][0])
    if 'protoparam' in parsed_params:
        result['protocol_param'] = decode_params(
            parsed_params['protoparam'][0])

    return result


def config_from_url(url):
    config = DEFAULT_CONFIG.copy()
    config.update(parse_url(url))
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=None)
    parser.add_argument('--output', type=str, default=None)
    parser.add_argument('--url', type=str, default=None)
    ns = parser.parse_args()

    if ns.port:
        DEFAULT_CONFIG['local_port'] = ns.port
    if ns.url is None:
        url = input('Input url: ')
    else:
        url = ns.url
    config = config_from_url(url)

    if ns.output:
        with open(ns.output, mode='w', encoding='utf8') as f:
            json.dump(config, f, indent=4)
    else:  # stdout
        print(json.dumps(config))


if __name__ == "__main__":
    main()
