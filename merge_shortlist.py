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


WHITELIST = ['ELK', 'lELK', 'PNG', 'DAI', 'ETH', 'USDT', 'USDC', 'QUICK', 'WBTC', 'LINK', 'YTS', 'OLIVE', 'PEFI', 'AAVE', 'GHST', 'MUST', 'DEFI5', 'CC10', 'CEL', 'KRILL', 'MANA', 'SUSHI', 'SPORE', 'SFIN', 'SL3', 'SNOB', 'FUSDT', 'BOO', 'SPIRIT', 'BNB', 'ZOO', 'CREAM', 'ICE', 'YFI', 'DSTEIN', 'SHIBA', 'ARFV2', 'CXO', 'AZUKI', 'AVE', 'HUSKY', 'HUSD', 'FILDA', 'GOF', 'MKR', 'COW', 'HBTC', 'MDX', 'HBELT', 'HPT', 'PTD', 'XAVA', 'VSO', 'JOE', 'UNI', 'STAKE', 'HNY', 'AGVE', 'XCOMB', 'DXD', 'HAUS', 'UNCX', 'BTCB', 'BUSD', 'CAKE', 'BAKE', 'REEF', 'XRP', 'ADA', 'DOT', 'TRX', 'BELT', 'SHI3LD', 'WUSD', 'WEXPOLY', 'WAULTX', 'PCOMB', 'PAR', 'POLYDOGE', 'SURF', 'YAK', 'QI', 'AVME', 'SHERPA', 'RUGPULL', 'WILD', 'FOLIVE', 'FOX', 'COLD', 'DXD', 'MDEX', 'BANANA', 'TUNDRA', 'NUTS', 'WEX', 'KANA', 'SOTA', 'WAVE', 'WBTC.e', 'WETH.e', 'DAI.e', 'USDT.e', 'LINK.e', 'SUSHI.e', 'AAVE.e', 'DCAU', 'BRIGHT', 'XGTV2', 'GLIDE', 'PLT', 'SYMM', 'CRX', 'PHOTON', 'AVAI', 'ORCA', 'SING', 'RAREV2', 'PUNK', 'FUSD', 'GNO', 'CRV']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge Elk.Finance tokenlists')
    parser.add_argument('--output_list', '-o', required=True)
    parser.add_argument('--version')

    args = parser.parse_args()

    all_tokenlist = {}
    all_tokenlist['name'] = f'Elk Top Tokens'
    all_tokenlist['logoURI'] = 'https://raw.githubusercontent.com/elkfinance/tokens/main/logos/all/0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C/logo.png'
    all_tokenlist['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    all_tokenlist['keywords'] = ['elk', 'defi']
    all_tokenlist['tokens'] = []

    pathlist = Path('.').glob('*.tokenlist.json')
    for path in pathlist:
         path = str(path)
         if not path.startswith('all') and not path.startswith('top'):
             print(path)

             #all_tokenlist['keywords'].append(path.split('.')[0].lower())

             with open(path, 'r') as f:
                tokenlist = json.load(f)

                tokens = {}
                if 'tokens' in tokenlist:
                    for token in tokenlist['tokens']:
                        if token['symbol'] in WHITELIST:
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
