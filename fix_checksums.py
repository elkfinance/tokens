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
    'AVAX': 43114,
    'FTM': 250,
    'FTMTEST': 4002,
}

WETH = {
    'MUMBAI': '0x5B67676a984807a212b1c59eBFc9B3568a474F0a',
    'MATIC': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
    'FUJI': '0xd00ae08403B9bbb9124bB305C09058E32C39A48c',
    'AVAX': '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7',
    'FTMTEST': '0xf1277d1Ed8AD466beddF92ef448A132661956621',
    'FTM': '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',
}


if __name__ == '__main__':
    for d in os.listdir('logos'):
        for f in os.listdir('logos/' + d):
            cksum = Web3.toChecksumAddress(f)
            if f != cksum:
                original = 'logos/' + d + '/' + f
                correct = 'logos/' + d + '/' + cksum
                print(original, correct)
                os.rename(original, correct)
