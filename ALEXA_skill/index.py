#!/usr/bin/env python3
import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
if 'LD_LIBRARY_PATH' not in os.environ:
    try:
    	os.environ['LD_LIBRARY_PATH'] = CURRENT_DIR + '/LIB/libxml2'
    	os.execv(sys.argv[0], [''])
    except :
        raise Exception("Failed execv")
        sys.exit(1)

print (sys.argv[0])

from test import test_database_initialization

def lambda_handler(event, context):
    # TODO implement
    test_database_initialization.testing()
    return 'Hello from Lambda'

#lambda_handler("","")