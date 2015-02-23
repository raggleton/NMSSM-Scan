#!/bin/bash

for f in "$@"
do
	perl Analyse_scans.pl "$f"&
done
