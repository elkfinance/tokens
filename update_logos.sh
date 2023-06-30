#!/usr/bin/env bash

for chain in avax bttc matic ftm heco bsc xdai fuse mumbai fuji ftmtest hecotest arbitrum elastos moonriver ethereum harmony hoo iotex kcc okex kava telos cronos optimism arthera_testnet astar bitgert metis neon_devnet pulse q wan; do
	rsync -a logos/$chain/ logos/all/
done
