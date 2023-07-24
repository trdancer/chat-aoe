#! /bin/bash

set -a
PY_ENV='PRODUCTION'
STRINGS_FILE='./data/patch_85208_strings.json'
DATA_FILE='./data/patch_85208_data.json'
ARMOR_FILE='./data/patch_85208_armor.json'

python3 init.py

# start server
