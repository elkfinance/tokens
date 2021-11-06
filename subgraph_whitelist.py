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


if __name__ == '__main__':
    tokenfile = f'{sys.argv[1]}.tokenlist.json'
    print(tokenfile)
    with open(tokenfile, 'r') as f:
        tokens = json.load(f)['tokens']

    for token in tokens:
        address = token['address'].lower()
        symbol = token['symbol'].lower()
        print(f'  \'{address}\', // {symbol}')
