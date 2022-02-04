#!/usr/bin/env bash

for list in all top farms; do
	python3 merge_lists.py -o $list.tokenlist.json -s symbols_$list.txt -t $list
done

