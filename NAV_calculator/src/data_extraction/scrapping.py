import requests
import re
from datetime import datetime

def upload_data(DEPLOY=False ,text=None):

	assert text is not None

	if DEPLOY:
		url = 'https://investment-caluclate.herokuapp.com/query'
	else:
		url = 'http://127.0.0.1:5000/query'
	print requests.post(url, json={'main_id': '1', 'data': text}).text
	pass


def filter(text="120450;Axis Dynamic Bond Fund - Direct Plan - Half Yearly Dividend Option;11.6051;11.4890;11.6051;01-Aug-2016"):

	text = text.replace('Plan ' , 'Plan - ')
	filter_replace = { '- -': '-', '-': ' - ', '\r' :''}
	for key, value in filter_replace.iteritems():
		text = text.replace(key, value)

	filter_substitute = {'[ ]+': ' '}
	for key, value in filter_substitute.iteritems():
		text = re.sub(key, value, text)

	return text

def date_to_sec(date="06-Apr-2015"):

	replace_month = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06', 'Jul' : '07', 'Aug' : '08' , 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'}
	for key, value in replace_month.iteritems():
		date = date.replace(key, value)
	epoch = datetime.utcfromtimestamp(0)
	current_time = datetime.strptime(date, "%d - %m - %Y")
	current_time -= epoch
	current_time = int(current_time.total_seconds())
	return current_time

def parse_scrapped_data(text=None):

	assert text is not None
	output_data = []

	text = re.findall('\d;([^\n]+)', text)
	for i in text:
		i = filter(i)
		i = i.split(";")
		temp_output = {
			"fund_name" : i[0],
			"date" : date_to_sec(i[-1]),
			"NAV": float(i[1])
		}
		output_data.append(temp_output)
		del temp_output

	return output_data


def scrap_data(DEPLOY=False):

	if DEPLOY:
		x = requests.get('http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf=53&tp=1&frmdt=01-Apr-2015&todt=07-Aug-2017').text
		with open('testing_output/output.txt', 'w') as f:
			f.write(x)
	else:
		with open('testing_output/output.txt', 'r') as f:
			x = f.read()
			pass

	output = parse_scrapped_data(text=x)
	upload_data(DEPLOY=DEPLOY,text=output)
    #
	# fund_name = set(re.findall('\d;([^;\d\n]+)', x))
	# for i in sorted(fund_name):
	# 	print i
	# pass


scrap_data(DEPLOY=False)