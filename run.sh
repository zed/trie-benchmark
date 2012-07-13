#!/bin/sh
prefix=$(date +%Y%m%d%H%M)
./benchmark.py --prefix $prefix &&
make-figures.py --plot-only --prefix $prefix
