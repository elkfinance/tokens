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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find chainlist duplicates')
    parser.add_argument('--input_list', '-i', required=True)
    parser.add_argument('--version')

    args = parser.parse_args()

    chain_address_map = {}

    with open(args.input_list, 'r') as f:
        tokenlist = json.load(f)
        if 'tokens' in tokenlist:
            for token in tokenlist['tokens']:
                if token['chainId'] in chain_address_map and token['address'] in chain_address_map[token['chainId']]:
                    print('Duplicate token found', token)
                else:
                    if token['chainId'] not in chain_address_map:
                        chain_address_map[token['chainId']] = {}
                    chain_address_map[token['chainId']][token['address']] = token
                print(chain_address_map)
    print('Done!')

