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
    'HUOBIECO_TESTNET': 256,
    'HUOBIECO': 128,
    'REEF': 13939,
    'XDAI': 100,
    'FUSE': 122,
    'OPTIMISM': 10,
    'OPTIMISM_TESTNET': 69,
    'KUCOIN': 321,
    'KUCOIN_TESTNET': 322,
    'ETHERLITE': 111,
    'ETHEREUM_CLASSIC': 61,
    'ETHEREUM_CLASSIC_TESTNET': 62,
    'MOONBEAM': 1284,
    'MOONBEAM_TESTNET': 1287,
    'CLOVER': 124,
    'CLOVER_TESTNET': 123,
    'CELO': 42220,
    'ALFAJORES': 44787,
    'ARBITRUM_TESTNET': 421611,
    'ARBITRUM': 42161,
    'FLARE': 14,
    'FLARE_TESTNET': 16,
    'FUSION': 32659,
    'HARMONY': 1666600000,
    'OKEX': 66,
    'BINANCE_TESTNET': 97,
    'BINANCE': 56,
    'ROPSTEN': 3,
    'ETHEREUM': 1,
}

WETH = {
    'MUMBAI': '0x5B67676a984807a212b1c59eBFc9B3568a474F0a',
    'MATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
    'FUJI': '0xd00ae08403B9bbb9124bB305C09058E32C39A48c',
    'AVALANCHE': '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7',
    'FANTOM_TESTNET': '0xf1277d1Ed8AD466beddF92ef448A132661956621',
    'FANTOM': '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',
    'HUOBIECO_TESTNET': '0x7aF326B6351C8A9b8fb8CD205CBe11d4Ac5FA836',
    'HUOBIECO': '0x5545153CCFcA01fbd7Dd11C0b23ba694D9509A6F',
    'REEF': '0x0000000000000000000000000000000000000000',
    'XDAI': '0xe91d153e0b41518a2ce8dd3d7944fa863463a97d',
    'BINANCE_TESTNET': '0x094616F0BdFB0b526bD735Bf66Eca0Ad254ca81F',
    'BINANCE': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
    'ROPSTEN': '0x0a180A76e4466bF68A7F86fB029BEd3cCcFaAac5',
    'ETHEREUM': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
}

IGNORE = ['WAVAX', 'WMATIC', 'WFTM', 'WBNB', 'WETH', 'WHT', 'WxDAI']


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



