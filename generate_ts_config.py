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
    'AVALANCHE': 43114,
    'FANTOM': 250,
    'FANTOM_TESTNET': 4002,
    'HECO_TESTNET': 128,
    'HECO': 256,
}

WETH = {
    'MUMBAI': '0x5B67676a984807a212b1c59eBFc9B3568a474F0a',
    'MATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
    'FUJI': '0xd00ae08403B9bbb9124bB305C09058E32C39A48c',
    'AVALANCHE': '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7',
    'FANTOM_TESTNET': '0xf1277d1Ed8AD466beddF92ef448A132661956621',
    'FANTOM': '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',
    'HECO_TESTNET': '0x7aF326B6351C8A9b8fb8CD205CBe11d4Ac5FA836',
    'HECO': '0x5545153CCFcA01fbd7Dd11C0b23ba694D9509A6F',
}

IGNORE = ['WAVAX', 'WMATIC', 'WFTM', 'WBNB', 'WETH', 'WHT']


if __name__ == '__main__':
    tokens = []
    tokenfiles = (f for f in os.listdir() if f.endswith('.tokenlist.json'))
    for tokenfile in tokenfiles:
        print(tokenfile)
        with open(tokenfile, 'r') as f:
            tokens += json.load(f)['tokens']

    grouped_tokens = {}
    for token in tokens:
        if token['symbol'] not in grouped_tokens:
            grouped_tokens[token['symbol']] = {}
        grouped_tokens[token['symbol']][token['chainId']] = {'address': token['address'], 'decimals': token['decimals'], 'name': token['name']}

    for symbol, chain_details in sorted(grouped_tokens.items(), key=lambda x: x[0]):
        if symbol in IGNORE:
            continue
        safe_symbol = symbol
        if '+' in safe_symbol:
            safe_symbol = safe_symbol.replace('+', '_')
        if '-' in safe_symbol:
            safe_symbol = safe_symbol.replace('-', '_')
        if safe_symbol.startswith('$') or safe_symbol.startswith('0') or safe_symbol.startswith('1') or safe_symbol.startswith('2'):
            safe_symbol = '_' + safe_symbol
        print('export const %s: { [chainId in ChainId]: Token } = {' % safe_symbol)
        name = list(chain_details.items())[0][1]['name']
        decimals = list(chain_details.items())[0][1]['decimals']
        for chain_name, chain_id in CHAIN_IDS.items():
            #if chain_id in chain_details and name != chain_details[chain_id]['name']:
            #    raise ValueError('Mismatched names', name, chain_details[chain_id]['name'], 'for', chain_id)
            address = '\'%s\'' % chain_details[chain_id]['address'] if chain_id in chain_details else 'ZERO_ADDRESS'
            print(f'  [ChainId.{chain_name}]: new Token(ChainId.{chain_name}, {address}, {decimals}, \'{symbol}\', \'{name}\'),')
        print('}\n')



