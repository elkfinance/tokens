#!/usr/bin/env bash

cd logos
for chain in *; do
	cd $chain;
	for f in *; do cd $f; magick 'logo.png' -resize '256x256' 'logo.png'; cd ..; done
	cd ..
done
cd ..
