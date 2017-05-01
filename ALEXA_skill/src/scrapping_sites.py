import requests
import json

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

#this fucntion scraps the ongoing and future coding competitons 
def codeforces(DEPLOY = False):
	x = ""
	output = []

	if DEPLOY:
		x = requests.get("http://codeforces.com/api/contest.list?gym=false").text
	else:
		with open( CURRENT_DIR +'/input_codeforces.json','r') as f:
			x = f.read()
			pass
		pass

	j = json.loads(x)
	for i in j["result"]:
		if i["phase"] == "BEFORE" or i["phase"] == "CODING" :
			temp = {}
			temp["competiton_name"] = i["name"]
			temp["site_name"] = "codeforces"
			temp["datetime"] = i["startTimeSeconds"]
			temp["classification"] = "cp"
			temp["URL"] = " "
			output.append(temp)
			del temp

	return (output)
	pass




#print (codeforces(DEPLOY = False))