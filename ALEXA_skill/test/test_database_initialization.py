#!/usr/bin/env python
import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from database import initialize_db
from src import scrapping_sites

def testing():

	#This is the main variable which changed to true all the changes will take place 
	#everywhere in the code and the code is ready to be uploaded.
	DEPLOY = True

	x = initialize_db.DynamoDB('competitons', DEPLOY = DEPLOY)
	x.put_data(scrapping_sites.codeforces(DEPLOY = DEPLOY))
	x.put_data(scrapping_sites.codechef(DEPLOY = DEPLOY))
	x.get_data( {
					'competiton_name' : 'VK Cup 2017 - Wild Card Round 2',
					'datetime' : 1493220900
				})
	pass
