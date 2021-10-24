#!/bin/bash

# Starts up a jupyter notebook server with sources in python path so you can REPL the existing python scripts.
# For pythonpath ref to work, run this script from the root directory, NOT the bin/ directory

PYTHONPATH=$(pwd)/src:$PATH jupyter notebook
