#!/bin/bash
# This script installs all the requirements for the project

git clone https://github.com/Martinsos/edlib.git
cd edlib && make && sudo make install
python -m pip install edlib

git clone https://github.com/calacademy-research/minibar

git clone https://github.com/lh3/minimap2
cd minimap2 && make
