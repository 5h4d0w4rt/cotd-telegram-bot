#!/bin/bash
# decompress zlib-compressed data
set -e

python3 -c 'import sys,zlib; sys.stdout.write(zlib.decompress(sys.stdin.buffer.read()).decode())' <"$@"
