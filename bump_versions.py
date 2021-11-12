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
    parser = argparse.ArgumentParser(description='Bump Elk.Finance tokenlists versions')
    parser.add_argument('--version', required=True)

    args = parser.parse_args()

    pathlist = Path('.').glob('*.tokenlist.json')
    for path in pathlist:
         path = str(path)
         if not path.startswith('all'):
            with open(path, 'r') as f:
                tokenlist = json.load(f)

            m = re.match(r'(\d+)\.(\d+)\.(\d+)', args.version)
            if m is None:
                print(f'Invalid version: {args.version}!')
                sys.exit(-1)
            version = {'major': int(m.group(1)), 'minor': int(m.group(2)), 'patch': int(m.group(3))}
            tokenlist['version'] = version

            with open(path, 'w') as f:
                f.write(json.dumps(tokenlist, indent=4, sort_keys=True))

                print(f'New list written to {path}')
