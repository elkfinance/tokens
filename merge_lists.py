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


CHAIN_IDS = {
    'MUMBAI': 80001,
    'MATIC': 137,
    'FUJI': 43113,
    'AVAX': 43114,
    'FTMTEST': 4002,
    'FTM': 250,
    'HECOTEST': 256,
    'HECO': 128,
    'BSC': 56,
    'XDAI': 100,
    'FUSE': 122,
    'KCC': 321,
    'ARBITRUM': 42161,
    'HARMONY': 1666600000,
    'OKEX': 66,
    'IOTEX': 4689,
    'HOO': 70,
    'ELASTOS': 20,
    'MOONRIVER': 1285,
    'TELOS': 40,
    'CRONOS': 25,
    'ETHEREUM': 1,
}

WETH = {
    'MUMBAI': '0x5B67676a984807a212b1c59eBFc9B3568a474F0a',
    'MATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
    'FUJI': '0xd00ae08403B9bbb9124bB305C09058E32C39A48c',
    'AVAX': '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7',
    'FTMTEST': '0xf1277d1Ed8AD466beddF92ef448A132661956621',
    'FTM': '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',
    'HECOTEST': '0x7aF326B6351C8A9b8fb8CD205CBe11d4Ac5FA836',
    'HECO': '0x5545153CCFcA01fbd7Dd11C0b23ba694D9509A6F',
    'BSC': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
    'XDAI': '0xe91d153e0b41518a2ce8dd3d7944fa863463a97d',
    'FUSE': '0x0BE9e53fd7EDaC9F859882AfdDa116645287C629',
    'KCC': '0x4446Fc4eb47f2f6586f9fAAb68B3498F86C07521',
    'ARBITRUM': '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1',
    'HARMONY': '0xcF664087a5bB0237a0BAd6742852ec6c8d69A27a',
    'OKEX': '0x8F8526dbfd6E38E3D8307702cA8469Bae6C56C15',
    'IOTEX': '0xA00744882684C3e4747faEFD68D283eA44099D03',
    'HOO': '0x3EFF9D389D13D6352bfB498BCF616EF9b1BEaC87',
    'ELASTOS': '0x517E9e5d46C1EA8aB6f78677d6114Ef47F71f6c4',
    'MOONRIVER': '0x98878B06940aE243284CA214f92Bb71a2b032B8A',
    'TELOS': '0xD102cE6A4dB07D247fcc28F366A623Df0938CA9E',
    'CRONOS': '0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23',
    'ETHEREUM': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
}


LOGO_DIR = 'logos'


HOSTED_URL = 'https://raw.githubusercontent.com/elkfinance/tokens/main/'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge Elk.Finance tokenlists')
    parser.add_argument('--output_list', '-o', required=True)
    parser.add_argument('--version')

    args = parser.parse_args()

    all_tokenlist = {}
    all_tokenlist['name'] = f'Elk Tokens'
    all_tokenlist['logoURI'] = 'https://raw.githubusercontent.com/elkfinance/tokens/main/logos/all/0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C/logo.png'
    all_tokenlist['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    all_tokenlist['keywords'] = ['elk', 'defi']
    all_tokenlist['tokens'] = []

    pathlist = Path('.').glob('*.tokenlist.json')
    for path in pathlist:
         path = str(path)
         if not path.startswith('all'):
             print(path)

             #all_tokenlist['keywords'].append(path.split('.')[0].lower())

             with open(path, 'r') as f:
                tokenlist = json.load(f)

                tokens = {}
                if 'tokens' in tokenlist:
                    for token in tokenlist['tokens']:
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
