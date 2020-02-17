#!/bin/bash
ROOT_DIR=`pwd`
export PYTHONPATH=$PYTHONPATH:$ROOT_DIR
cd src/common_utils/database_preparing
CURR_DIR=`pwd`
export PYTHONPATH=$PYTHONPATH:$CURR_DIR
python3 set_init_configure.py
cd ../../..

