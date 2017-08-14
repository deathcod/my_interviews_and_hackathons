import json
import re

import lxml
import requests
from lxml import html


def scrap_wiki_african_cup_of_nation(DEPLOY=False):
	if DEPLOY:
		x = requests.get('https://en.wikipedia.org/wiki/Africa_Cup_of_Nations').text
	else:
		with open('testing_sites/Africa_Cup_of_Nations.html', 'r') as f:
			x = f.read()
			pass
		pass

	tree = html.fromstring(x)

	def country_detail(flag_path, url_path, name_path):
		path = "//table[@class='wikitable'][1]/tr[position()>=29 and position()<=35]"

		out = {
			'flag': tree.xpath(path + flag_path),
			'url': tree.xpath(path + url_path),
			'name': tree.xpath(path + name_path)
		}
		return out

	def score_detail(score_path):
		path = "//table[@class='wikitable'][1]/tr[position()>=29 and position()<=35]"
		temp_score = tree.xpath(path + score_path)
		return [re.findall('\d+-\d+', lxml.html.tostring(i).replace('&#8211;', '-')) for i in temp_score]

	output = {
		'host_country': country_detail('/td[2]/span/img/@src', '/td[2]/a/@href', '/td[2]/a/text()'),
		'country_1': country_detail('/td[3]/b/img/@src', '/td[3]/b/a/@href', '/td[3]/b/a/text()'),
		'score_1': score_detail('/td[4]'),
		'country_2': country_detail('/td[5]/img/@src', '/td[5]/a/@href', '/td[5]/a/text()'),
		'country_3': country_detail('/td[6]/img/@src', '/td[6]/a/@href', '/td[6]/a/text()'),
		'score_2': score_detail('/td[7]'),
		'country_4': country_detail('/td[8]/img/@src', '/td[8]/a/@href', '/td[8]/a/text()')
	}

	del(output["host_country"]["flag"][5])
	del (output["host_country"]["url"][5])
	del (output["host_country"]["name"][5])

	# test if 7 values and not null
	return output


def african_cup_detail_per_year(DEPLOY=False, year=2006):
	if DEPLOY:
		x = requests.get('https://en.wikipedia.org/wiki/' + str(year) + '_Africa_Cup_of_Nations').text
		x = x.split(' ')
		x = ' '.join(i.encode('ascii', 'ignore') for i in x)
	else:
		with open('testing_sites/' + str(year) + '_Africa_Cup_of_Nations.html', 'r') as f:
			x = f.read()
			pass
		pass

	tree = html.fromstring(x)
	logo = tree.xpath('/html/body/div[3]/div[3]/div[4]/div/table[1]/tr[2]/td/a/img/@src')

	def players():

		attendee = tree.xpath('//td[@class="attendee"]')

		out2 = {
			'top-scorer': {
				'country': attendee[0].xpath('span/a/@title'),
				'player-name': attendee[0].xpath('a/@title'),
				'goals-scored': re.findall('\d+ goals', lxml.html.tostring(attendee[0]))[0]
			},
			'best-player': {
				'country': attendee[1].xpath('span/a/@title'),
				'player-name': attendee[1].xpath('a/@title')
			}
		}
		return out2

	def stadium():
		venue_table = re.findall(
			'(id="Venues"[\s\w<>=\"-:?@.;()%!\[\]/]+?<table class="wikitable"[\s\w<>=\"-:?@.;()%!\[\]]+?</table>)', x,
			re.UNICODE)[0]

		out1 = {
			'city': re.findall('<th(?: width="160"| colspan="3"| colspan="2")?><a href="([^"]+?)" title="([^"]+?)">',
							   venue_table),
			'capacity': re.findall('Capacity: (?:<b>)?([^<]+?)<', venue_table),
			'stadium_name': re.findall('<td(?: colspan="2"| colspan="3")?><a href="([^"]+?)".*?title="([^"]+?)">',
									   venue_table)
		}
		return out1

	output = {
		'logo': logo,
		'player': players(),
		'stadium': stadium()
	}
	return output


def get_pic_url(DEPLOY=False, query_word=''):
	assert query_word != ''
	path = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch&sa=X&sqi=2&ved=0ahUKEwi87dq4gJjVAhWnhVQKHSHnCmUQ_AUIBygC&biw=1366&bih=671"

	if DEPLOY:
		x = requests.get(path % (query_word.replace(' ', '+'))).text
		'''
		with open('testing_sites/google_query_image.html', 'w') as f:
			f.write(x)
			pass
		'''
	else:
		with open('testing_sites/google_query_image.html', 'r') as f:
			x = f.read()
			pass
		pass
	return re.findall('src="(https://[^"]+)?"', x)[1]


def get_wiki_page_description(DEPLOY=False, title=''):
	assert title != ''
	path = 'https://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=extracts&format=json&exsentences=1'
	if DEPLOY:
		x = requests.get(path % (title)).text
		# with open('testing_sites/wiki_page_description.html', 'w') as f:
		# 	f.write(x)
		# 	pass
	else:
		with open('testing_sites/wiki_page_description.html', 'r') as f:
			x = f.read()
			pass
		pass

	# crashes if doesnt find the value please look to it
	wiki_json = json.loads(x)
	pages = wiki_json['query']['pages']

	# couldnot find the description
	if '-1' in pages:
		return "--"

	for key in pages:
		return pages[key]['extract']


def pretty_print_json(json_data):
	print json.dumps(json_data, indent=4, sort_keys=True)
	pass

if __name__ == '__main__':
	# print get_pic_url(DEPLOY=True, query_word="tanmay rakshit")
	print get_wiki_page_description(DEPLOY=True, title='Estdio 11 de Novembro')
	# pretty_print_json(african_cup_detail_per_year(DEPLOY=False))
	#pretty_print_json(scrap_wiki_african_cup_of_nation())
