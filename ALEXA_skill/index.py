#!usr/bin/env
import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from test import test_database_initialization

def lambda_handler(event, context):
    # TODO implement
    test_database_initialization.testing()
    return 'Hello from Lambda'

#lambda_handler("","")