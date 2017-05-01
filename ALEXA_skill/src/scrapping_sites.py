import requests
import json
from lxml import html
from datetime import datetime

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
	del x,j
	return (output)
	pass


def codechef(DEPLOY = False):

	#TODO there is also UPCOMING Contest so do scrap it too.
	x = ""
	output = []
	if DEPLOY :
		x = requests.get("https://www.codechef.com/contests").text
	else:
		with open( CURRENT_DIR +'/input_codechef.html','r') as f:
			x = f.read()
			pass
		pass

	tree = html.fromstring(x)

	competiton_name_list = tree.xpath('//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[2]/a')
	datetime_list = tree.xpath('//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[3]')
	URL_list = tree.xpath('//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[2]/a/@href')
	length = len(competiton_name_list)
	
	for i in range(length):

		temp = {}
		temp["competiton_name"] = competiton_name_list[i].text_content()
		temp["site_name"] = "codechef"
		temp["datetime"] = datetime_list[i].text_content()
		epoch = datetime.utcfromtimestamp(0)
		temp["datetime"] = datetime.strptime(temp["datetime"], "%d %b %Y  %H:%M:%S")
		temp["datetime"] -= epoch
		temp["datetime"] = int(temp["datetime"].total_seconds())
		temp["classification"] = "cp"
		temp["URL"] = "https://www.codechef.com" + URL_list[i]
		output.append(temp)
		del temp

	del x,tree,competiton_name_list,datetime_list,URL_list,length
	return output
	
	'''
	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[1]/td[1]
	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[1]/td[2]/a
	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[1]/td[3]
	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[1]/td[4]


	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[2]/td[1]
	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[2]/td[2]/a
	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[2]/td[3]
	//*[@id="primary-content"]/div/div[3]/table/tbody/tr[2]/td[4]
	'''

#codechef()
#print (codeforces(DEPLOY = False))
