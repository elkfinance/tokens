#!/usr/bin/python3

import argparse
import csv
from datetime import datetime
import itertools
import json
import pandas
import requests
import shutil
import os
import re
import sys
from web3 import Web3


CHAIN_IDS = {
    'MUMBAI': 80001,
    'MATIC': 137,
    'FUJI': 43113,
    'AVAX': 43114
}

WETH = {
    'MUMBAI': '0x5B67676a984807a212b1c59eBFc9B3568a474F0a',
    'MATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
    'FUJI': '0xd00ae08403B9bbb9124bB305C09058E32C39A48c',
    'AVAX': '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7'
}


LOGO_DIR = 'logos'


HOSTED_URL = 'https://raw.githubusercontent.com/elkfinance/tokens/main/'


def process_token(t, chain, fetch_logo):
    chainId = CHAIN_IDS[chain.upper()]
    if t['chainId'] == chainId:
        address = Web3.toChecksumAddress(t['address'])
        path = os.path.join(chain.lower(), t['address'], 'logo.png')
        logo_path = os.path.join(LOGO_DIR, path)
        logo_target = os.path.join(HOSTED_URL, logo_path)
        if fetch_logo:
            download_logo(t['logoURI'], logo_path)
        t['address'] = address
        t['logoURI'] = logo_target
        return [t]
    else:
        return []


def download_logo(url, path):
    print(f'Downloading logo from {url} to {path}...', end='')
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    r = requests.get(url, allow_redirects=True)
    with open(path, 'wb') as f:
        f.write(r.content)
    print(' Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage Elk.Finance tokens')
    parser.add_argument('--chain', '-c', required=True)
    parser.add_argument('--output_list', '-o', required=True)
    parser.add_argument('--url', '-u')
    parser.add_argument('--logos', '-l', default=False, action='store_true')
    parser.add_argument('--version')

    args = parser.parse_args()

    chain = args.chain.upper()
    if chain not in CHAIN_IDS:
        print(f'Unknown chain: {chain}!')
        sys.exit(-1)

    with open(args.output_list, 'r') as f:
        old_tokenlist = json.load(f)

    if args.url is not None:
        new_tokenlist = requests.get(args.url).json()
    else:
        new_tokenlist = {}

    tokenlist = {}
    tokenlist['name'] = f'Elk {chain} Tokens'
    tokenlist['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    tokenlist['keywords'] = ['elk', 'defi', chain.lower()]

    if args.version is not None:
        m = re.match(r'(\d+)\.(\d+)\.(\d+)', args.version)
        if m is None:
            print(f'Invalid version: {args.version}!')
            sys.exit(-1)
        version = {'major': int(m.group(1)), 'minor': int(m.group(2)), 'patch': int(m.group(3))}
    else:
        try:
            old_version = old_tokenlist['version']
            version = old_version
            version['minor'] += 1
            version['patch'] = 0
        except:
            version = {'major': 1, 'minor': 0, 'patch': 0}
    tokenlist['version'] = version

    tokens = {}

    if 'tokens' in old_tokenlist:
        for token in old_tokenlist['tokens']:
            tokens[token['address'].lower()] = token

    if 'tokens' in new_tokenlist:
        for token in new_tokenlist['tokens']:
            tokens[token['address'].lower()] = token

    tokenlist['tokens'] = list(itertools.chain(*[process_token(t, chain, args.logos) for t in tokens.values()]))

    list_logo = None
    for token in tokenlist['tokens']:
        if token['address'] == WETH[chain]:
            list_logo = token['logoURI']
            break
    tokenlist['logoURI'] = list_logo

    with open(args.output_list, 'w') as f:
        f.write(json.dumps(tokenlist, indent=4, sort_keys=True))

    print(f'New list written to {args.output_list}')

