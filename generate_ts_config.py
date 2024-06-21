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

WHITELIST = [ 'PNG', 'DAI', 'ETH', 'USDT', 'USDC', 'QUICK', 'WBTC', 'LINK', 'YTS', 'OLIVE', 'PEFI', 'AAVE', 'GHST', 'MUST', 'DEFI5', 'CC10', 'CEL', 'KRILL', 'MANA', 'SUSHI', 'SPORE', 'SFIN', 'SL3', 'SNOB', 'FUSDT', 'BOO', 'SPIRIT', 'BNB', 'ZOO', 'CREAM', 'ICE', 'YFI', 'DSTEIN', 'SHIBA', 'ARFV2', 'CXO', 'AZUKI', 'AVE', 'HUSKY', 'HUSD', 'FILDA', 'GOF', 'MKR', 'COW', 'HBTC', 'MDX', 'HBELT', 'HPT', 'PTD', 'XAVA', 'VSO', 'JOE', 'UNI', 'STAKE', 'HNY', 'AGVE', 'XCOMB', 'DXD', 'HAUS', 'UNCX', 'BTCB', 'BUSD', 'CAKE', 'BAKE', 'REEF', 'XRP', 'ADA', 'DOT', 'TRX', 'BELT', 'SHI3LD', 'WUSD', 'WEXPOLY', 'WAULTX', 'PCOMB', 'PAR', 'POLYDOGE', 'SURF', 'YAK', 'QI', 'AVME', 'SHERPA', 'RUGPULL', 'WILD', 'FOLIVE', 'FOX', 'COLD', 'DXD', 'MDEX', 'BANANA', 'TUNDRA', 'NUTS', 'WEX', 'KANA', 'SOTA', 'WAVE', 'WBTC.e', 'WETH.e', 'DAI.e', 'USDT.e', 'LINK.e', 'SUSHI.e', 'AAVE.e', 'DCAU', 'BRIGHT', 'XGTV2', 'GLIDE', 'PLT', 'SYMM', 'CRX', 'PHOTON', 'AVAI', 'ORCA', 'SING', 'RAREV2', 'PUNK', 'FUSD', 'GNO', 'CRV', 'MAI', 'RACEX', 'AUTO', 'METX', 'MELT', 'H2O', 'USDC.e', 'TEDDY', 'CHARM', 'KBN', 'GIV', 'ISA', 'RADI', 'LOST', 'KACY', 'PDDOLLAR', 'PDSHARE', 'LYD', 'SFI', 'HAKU', 'KLO', 'RADIO']

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
    'IOTEX': 4689,
    'HOO': 70,
    'ELAETH': 20,
    'TELOS': 40,
    'CRONOS': 25,
    'KAVA': 2222,
    'MOONRIVER': 1285,
    'BINANCE_TESTNET': 97,
    'BINANCE': 56,
    'ROPSTEN': 3,
    'ETHEREUM': 1,
    'KAVA' : 2222,
    'BTTC' : 199,
    'BTTC_TESTNET' : 1029,
    'ARTHERA_TESTNET' : 10243,
    'ARTHERA' : 10242,
    'ASTAR' :  592,
    'BITGERT' : 32520,
    'METIS' : 1088,
    'Q' : 35441,
    'WAN' : 888,
    'NEON_DEVNET' : 245022926,
    'NEON' : 245022934,
    'VELAS' : 106,
    'BASE' : 8453,
    'LINEA' : 59144,
	'ROOTSTOCK': 30,
	'BOBAETH': 288,
	'BOBABNB': 56288,
	'CLOVER': 1024,
	'AURORA': 1313161554,
	'ZKSYNCERA': 324,
	'SCROLL': 534352,
	'BLAST': 81457,
	'OPBNB': 204,
	'MANTLE': 5000,
	'POLYGONZKEVM': 1101,}

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
    'FUSE': '0x0BE9e53fd7EDaC9F859882AfdDa116645287C629',
    'KUCOIN': '0x4446Fc4eb47f2f6586f9fAAb68B3498F86C07521',
    'ARBITRUM': '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1',
    'HARMONY': '0xcF664087a5bB0237a0BAd6742852ec6c8d69A27a',
    'OKEX': '0x8F8526dbfd6E38E3D8307702cA8469Bae6C56C15',
    'IOTEX': '0xA00744882684C3e4747faEFD68D283eA44099D03',
    'HOO': '0x3EFF9D389D13D6352bfB498BCF616EF9b1BEaC87',
    'ELAETH': '0x517E9e5d46C1EA8aB6f78677d6114Ef47F71f6c4',
    'MOONRIVER': '0x98878B06940aE243284CA214f92Bb71a2b032B8A',
    'TELOS': '0xD102cE6A4dB07D247fcc28F366A623Df0938CA9E',
    'CRONOS': '0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23',
    'BINANCE_TESTNET': '0x094616F0BdFB0b526bD735Bf66Eca0Ad254ca81F',
    'BINANCE': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
    'ROPSTEN': '0x0a180A76e4466bF68A7F86fB029BEd3cCcFaAac5',
    'ETHEREUM': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    'KAVA' : '0xc86c7C0eFbd6A49B35E8714C5f59D99De09A225b',
    'BTTC' : '0x8D193c6efa90BCFf940A98785d1Ce9D093d3DC8A',
    'BTTC_TESTNET' : '0x107742EB846b86CEaAF7528D5C85cddcad3e409A',
    'ARTHERA_TESTNET' : '0x5A1750f9cb8A7E98e1FD618922Af276493318710',
    'ARTHERA' : '0x69D349E2009Af35206EFc3937BaD6817424729F7',
    'ASTAR' :  '0xAeaaf0e2c81Af264101B9129C00F4440cCF0F720',
    'BITGERT' : '0x0eb9036cbE0f052386f36170c6b07eF0a0E3f710',
    'METIS' : '0x75cb093E4D61d2A2e65D8e0BBb01DE8d89b53481',
    'NEON_DEVNET' : '0x11adc2d986e334137b9ad0a0f290771f31e9517f',
    'NEON' : '0x202C35e517Fa803B537565c40F0a6965D7204609',
    'Q' : '0xd07178e3eCbC78De110Df84fe1A979D5f349784a',
    'WAN' : '0xdabD997aE5E4799BE47d6E69D9431615CBa28f48',
    'VELAS' : '0xc579D1f3CF86749E05CD06f7ADe17856c2CE3126',
    'BASE' : '0x4200000000000000000000000000000000000006',
    'LINEA' : '0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f',
	'ROOTSTOCK': '0x542FDA317318eBf1d3DeAF76E0B632741a7e677d',
	'BOBAETH': '0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000',
	'BOBABNB': '0x4200000000000000000000000000000000000023',
	'CLOVER': '0x1376C97C5c512d2d6F9173A9A3A016B6140b4536',
	'CELO': '0x471EcE3750Da237f93B8E339c536989b8978a438',
	'AURORA': '0x8BEc47865aDe3B172A928df8f990Bc7f2A3b9f79',
	'ZKSYNCERA': '0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91',
	'SCROLL': '0x5300000000000000000000000000000000000004',
	'BLAST': '0x4300000000000000000000000000000000000004',
	'OPBNB': '0x4200000000000000000000000000000000000006',
	'MOONBEAM': '0xAcc15dC74880C9944775448304B263D191c6077F',
	'MANTLE': '0x78c1b0C915c4FAA5FffA6CAbf0219DA63d7f4cb8',
	'POLYGONZKEVM': '0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9',}

IGNORE = ['WAVAX', 'WMATIC', 'WFTM', 'WBNB', 'WETH', 'WHT', 'WxDAI', 'WFUSE', 'WKCS', 'WARETH', 'WONE', 'WOKT', 'WIOTX', 'WHOO', 'WELA', 'WMOVR', 'WTLOS', 'WCRO', 'WKAVA', 'WBTT', 'WAA', 'WASTAR', 'WBRISE', 'WMETIS', 'WNEON', 'WQ', 'WWAN', 'WVLX', 'WRBTC', 'WCLV', 'CELO', 'AURORA', 'WGLMR', 'WMNT']


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
        if symbol not in WHITELIST:
            continue
        safe_symbol = symbol
        if '+' in safe_symbol:
            safe_symbol = safe_symbol.replace('+', '_')
        if '-' in safe_symbol:
            safe_symbol = safe_symbol.replace('-', '_')
        if '.' in safe_symbol:
            safe_symbol = safe_symbol.replace('.', '_')
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



