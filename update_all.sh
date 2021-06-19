#!/usr/bin/env bash

python update_list.py -o avax.tokenlist.json -c avax -u https://raw.githubusercontent.com/pangolindex/tokenlists/main/aeb.tokenlist.json --logos
python update_list.py -o matic.tokenlist.json -c matic -u https://unpkg.com/quickswap-default-token-list@1.0.54/build/quickswap-default.tokenlist.json --logos
#python update_list.py -o matic.tokenlist.json -c matic -u https://unpkg.com/@cometh-game/default-token-list@latest/build/comethswap-default.tokenlist.json --logos
python update_list.py -o ftm.tokenlist.json -c ftm --logos
python update_list.py -o heco.tokenlist.json -c heco -u https://raw.githubusercontent.com/mdexSwap/hswap/main/tokenlist.json --logos
python update_list.py -o mumbai.tokenlist.json -c mumbai --logos
python update_list.py -o fuji.tokenlist.json -c fuji --logos
python update_list.py -o ftmtest.tokenlist.json -c ftmtest --logos
python update_list.py -o hecotest.tokenlist.json -c hecotest --logos

for chain in avax matic ftm heco mumbai fuji ftmtest hecotest; do
	rsync -a logos/$chain/ logos/all/
done
