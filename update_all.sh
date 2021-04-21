#!/usr/bin/env bash

python update_list.py -o avax.tokenlist.json -c avax -u https://raw.githubusercontent.com/pangolindex/tokenlists/main/aeb.tokenlist.json --logos
python update_list.py -o matic.tokenlist.json -c matic -u https://unpkg.com/quickswap-default-token-list@1.0.54/build/quickswap-default.tokenlist.json --logos
python update_list.py -o mumbai.tokenlist.json -c mumbai --logos
python update_list.py -o fuji.tokenlist.json -c fuji --logos

for chain in avax matic mumbai fuji; do
	rsync -a logos/$chain/ logos/all/
done
