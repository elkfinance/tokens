#!/usr/bin/env bash

for list in all top farms; do
	python merge_lists.py -o $list.tokenlists.json -s symbols_$list.txt
done

