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
    for d in os.listdir('logos'):
        for f in os.listdir('logos/' + d):
            cksum = Web3.to_checksum_address(f)
            if f != cksum:
                original = 'logos/' + d + '/' + f
                correct = 'logos/' + d + '/' + cksum
                print(original, correct)
                os.rename(original, correct)
