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

from pathlib import Path


IGNORE_LISTS = ['all', 'top', 'farms', 'unverified']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge Elk.Finance tokenlists')
    parser.add_argument('--symbols', '-s')
    parser.add_argument('--output_list', '-o', required=True)
    parser.add_argument('--list_title', '-t', required=True)
    parser.add_argument('--version')

    args = parser.parse_args()

    if args.symbols:
        with open(args.symbols) as file:
            whitelist = [line.rstrip() for line in file]
    else:
        whitelist = None

    all_tokenlist = {}
    all_tokenlist['name'] = f'Elk {args.list_title.title()} Tokens'
    all_tokenlist['logoURI'] = 'https://raw.githubusercontent.com/elkfinance/tokens/main/logos/all/0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE/logo.png'
    all_tokenlist['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    all_tokenlist['keywords'] = ['elk', 'defi']
    all_tokenlist['tokens'] = []

    added_tokens = {}

    pathlist = Path('.').glob('*.tokenlist.json')
    for path in pathlist:
         path = str(path)
         if not any([path.startswith(l) for l in IGNORE_LISTS]):
             print(path)

             #all_tokenlist['keywords'].append(path.split('.')[0].lower())

             with open(path, 'r') as f:
                tokenlist = json.load(f)

                tokens = {}
                if 'tokens' in tokenlist:
                    for token in tokenlist['tokens']:
                        if whitelist and token['symbol'] in whitelist or not whitelist:
                            if token['chainId'] in added_tokens and token['address'] in added_tokens[token['chainId']]:
                                print(f'Token {token} is a duplicate! Ignoring...')
                            else:
                                if token['chainId'] not in added_tokens:
                                    added_tokens[token['chainId']] = {}
                                added_tokens[token['chainId']][token['address']] = token
                                clean_token = {'address': token['address'], 'chainId': token['chainId'], 'decimals': token['decimals'], 'logoURI': token['logoURI'], 'name': token['name'], 'symbol': token['symbol']}
                                tokens[clean_token['address'].lower()] = clean_token
                all_tokenlist['tokens'] = all_tokenlist['tokens'] + list(tokens.values())

    if args.version is not None:
        m = re.match(r'(\d+)\.(\d+)\.(\d+)', args.version)
        if m is None:
            print(f'Invalid version: {args.version}!')
            sys.exit(-1)
        version = {'major': int(m.group(1)), 'minor': int(m.group(2)), 'patch': int(m.group(3))}
    else:
        try:
            with open(args.output_list, 'r') as f:
                old_tokenlist = json.load(f)
                old_version = old_tokenlist['version']
                version = old_version
                version['minor'] += 1
                version['patch'] = 0
        except:
            version = {'major': 1, 'minor': 0, 'patch': 0}
    all_tokenlist['version'] = version

    with open(args.output_list, 'w') as f:
        f.write(json.dumps(all_tokenlist, indent=4, sort_keys=True))

    print(f'New list written to {args.output_list}')
