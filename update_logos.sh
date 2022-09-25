#!/usr/bin/env bash

for chain in avax matic ftm heco bsc xdai fuse mumbai fuji ftmtest hecotest arbitrum elastos moonriver ethereum harmony hoo iotex kcc okex telos cronos optimism kava; do
	rsync -a logos/$chain/ logos/all/
done
