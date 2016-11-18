#!/usr/bin/python
import nltk
import re
import pprint
#import requests
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import urllib

class extraction(object):

	"""docstring for extraction"""

	def __init__(self, url):
		self.url = url

	def extract(self):
		self.text = urllib.urlopen(self.url).read()

	def export_file(self,txt):
		file(txt,'w').write(self.text)

	def import_file(self,txt):
		self.text=file(txt,'r').read()

	def create_text(self,write):
		self.text = self.text.decode('utf-8','replace')
		z=re.findall('([\d]{4})[\s]*([\w,\'; ]*)[\s]*by William Shakespeare([\s\w<>=\"-:?@.;()%!\[\]|]*?THE END)',self.text)
		if write:
			for i in z:
				file(i[1]+".txt",'w').write(i[2])
		return z
	pass

class database(object):

	"""docstring for database"""

	def __init__(self,database):
		client = MongoClient()
		self.db=client[database]

	def get_all_doc(self,collection,where,columns):
		collection = self.db[collection]
		return [i for i in collection.find(where,columns)]
		
	def get_first(self,collection,where,columns):
		collection = self.db[collection]
		return collection.find_one(where,columns)
	
	def insert(self,collection,val):
		collection = self.db[collection]
		val['_id']=collection.count() + 1
		collection.insert(val)

	def delete(self,collection,where):
		collection = self.db[collection]
		collection.remove(where)

	def store_files(self,ext_text):
		post=dict()
		for i in ext_text:
			post['year']=i[0].encode('utf-8','replace')
			post['name']=i[1].encode('utf-8','replace')
			post['text']=i[2].encode('utf-8','replace')
			self.insert('play',post)
			pass

	def store_names(self,dic_name):
		post=dict()
		for i in dic_name:
			post['name']=i
			post['plays']=list(set(dic_name[i]))
			self.insert('naam',post)
			pass

	def store_place(self,dic_place):
		post=dict()
		for i in dic_place:
			post['place']=i
			post['plays']=list(set(dic_place[i]))
			self.insert('plaace',post)
			pass

	def store_relationship(self,dic_rela):
		for i in dic_rela:
			self.insert('relationship',dic_rela[i])
			pass

	def get_name_plays(self,name):
		name=name.upper()
		plays=self.get_first('naam',{'name':name},{'plays':1})
		if len(plays) != 0:
			return plays
		else:
			return {'text':'No data found'}
		pass

	def get_place_plays(self,place):
		place=place.lower()
		plays=self.get_first('plaace',{"place":place},{"plays":1})
		if len(plays) != 0:
			return plays
		else:
			return {'text':'No data found'}
		pass

	def get_relationship(self,name1,name2):
		name1 = name1.lower()
		name2 = name2.lower()
		
		relation = self.get_all_doc('relationship',{'$and':[{'name1':name1},{'name2':name2}]},{'play':1,'relation':1})
		
		if len(relation) == 0:
			relation = self.get_all_doc('relationship',{'$and':[{'name1':name2},{'name2':name1}]},{'play':1,'relation':1})

		if len(relation) != 0:
			return relation
		else:
			return {'text':'No data found'}
	pass

class word_featuring(object):

	"""docstring for word_featuring"""

	def __init__(self, extract,data):
		self.x=extract
		self.y=data

	def tagging(self,text):
		#document=self.y.get_first('play',where,{"text":1})
		document=text
		sentences = nltk.sent_tokenize(document)
		sentences = [nltk.word_tokenize(sent) for sent in sentences]
		sentences = [nltk.pos_tag(sent) for sent in sentences]
		return sentences	

	def chuncking(self,text,regex):
		s=list()
		cp = nltk.RegexpParser(regex)
		for sent in self.tagging(text):
			tree = cp.parse(sent)
			for subtree in tree.subtrees():
				if subtree.label() == 'NP': s.append(subtree)
		return s
	def filter(self,text):
		sent="""<<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAM
SHAKESPEARE IS COPYRIGHT 1990-1993 BY WORLD LIBRARY, INC., AND IS
PROVIDED BY PROJECT GUTENBERG ETEXT OF ILLINOIS BENEDICTINE COLLEGE
WITH PERMISSION.  ELECTRONIC AND MACHINE READABLE COPIES MAY BE
DISTRIBUTED SO LONG AS SUCH COPIES (1) ARE FOR YOUR OR OTHERS
PERSONAL USE ONLY, AND (2) ARE NOT DISTRIBUTED OR USED
COMMERCIALLY.  PROHIBITED COMMERCIAL DISTRIBUTION INCLUDES BY ANY
SERVICE THAT CHARGES FOR DOWNLOAD TIME OR FOR MEMBERSHIP.>>"""

		sent=sent.split('\n')
		for i in sent:
			text=text.replace(i,'')

		garbage = ['ACT','EPILOGUE','THE END','DRAMATIS PERSONAE','Dramatis Personae','.']
		for i in garbage:
			text = text.replace(i,'')
		text = re.sub(r'(scene|SCENE|Scene)','?*?',text)
		text = re.sub(r'[ ]+',' ',text)
		text = re.sub(r'(\s){2,}','\n',text)
		text = re.sub(r' and ',',',text)
		return text


	def names(self):

		names = list()
		post = dict()

		for i in self.y.get_all_doc('play',{},{"text":1,"name":1}):
			text = i['text'].decode('utf-8','replace')
			text = self.filter(text)
			sent = re.findall(r'([A-Z]{4,}[A-Z ]*)',text)
			sent = set(sent)
			new_sent = list()

			for j in sent:
				s=j.split('     ')
				new_sent = new_sent + [k.strip() for k in s if i!='']

			new_sent = set(new_sent)

			for j in new_sent:
				if j=='':
					continue
				if j not in names:
					j=j.encode('utf-8','replace')
					post[j] = list()
					names.append(j)
				post[j].append(i['name'].encode('utf-8','replace'))
			
		return post

	def place(self):

		names = list()
		post = dict()

		for k in self.y.get_all_doc('play',{},{"text":1,"name":1}):

			text = k['text'].decode('utf-8','replace')
			text = self.filter(text)
			tagged_word = self.tagging(text)
			new_list = list()

			for i in tagged_word:
				for j in i:
					if j[1]=='NNP':
						new_list.append(j[0].lower().decode('utf-8','replace'))

			new_list=list(set(new_list))

			new_list = [i.decode('utf-8','replace') for i in new_list if i not in stopwords.words()]

			flag=0
			place=list()
			for i in new_list:
				for synset in wn.synsets(i):
					sent=synset.definition()
					if re.findall(r'(?i) city|country|town',sent):
						place.append(i)

			for j in place:
				if j=='':
					continue
				if j not in names:
					j=j.encode('utf-8','replace')
					post[j] = list()
					names.append(j)
				post[j].append(k['name'].encode('utf-8','replace'))

		file('place.txt','w').write('\n'.join(names))
		#return post

	def relationship(self):

		t = self.y.get_all_doc('play',{'$and':[{'_id':{'$ne':1}},{'_id':{'$ne':36}}]},{'text':1,'name':1})
		s=''
		for i,out_txt in enumerate(t): 
			text = self.filter(out_txt['text'].decode('utf-8','ignore'))
			text = text[:text.find('?*?')]
			t[i]['text'] = text 


		for j,out_txt in enumerate(t):
			text = out_txt['text'] 
			text = text.split('\n')
			for i,txt in enumerate(text):
				words = txt.split(' ')
				if '\"' in words:
					cw = words.count('\"')
					pre_txt = text[i-1]
					pre_words = pre_txt.split(' ')
					want_words = pre_words[-cw:]
					curr_words = words[:len(words)-cw]
					curr_words += want_words
					text[i] = ' '.join(curr_words)
			t[j]['text'] = '\n'.join(text)


		for j,out_txt in enumerate(t):
			
			alert = False
			alert_txt = ''
			
			if out_txt['_id'] in [10,28,30,31,32]:
				text = out_txt['text']
				text = text.split('\n')
				for i,txt in enumerate(text):
					
					if alert == True:
						if ',' not in txt and txt.isupper() and txt!='':
							txt = txt+", "+alert_txt
						else:
							alert = False
							alert_txt = ''

					if ',' not in txt and not txt.isupper() and txt!='':
						alert_txt = txt
						alert = True

					text[i] = txt
				t[j]['text'] = '\n'.join(text)

		for j,out_txt in enumerate(t):

			text = out_txt['text']
			text = text.split('\n')
			for i,txt in enumerate(text):
				txt_srch = re.search(r'(?i) ([^\' ]*)?\'(?:s|S) ([^ ,]*)',txt)
				if txt_srch:
					txt = re.sub(r'(?i) ([^\' ]*)?\'(?:s|S) ([^ ,]*)'," "+txt_srch.group(2)+" of "+txt_srch.group(1),txt)
				
				txt_srch = re.search(r'(?i) his ([^ ,]*)',txt)
				if txt_srch:
					name_pre = text[i-1][:text[i-1].find(',')]
					txt = re.sub(r'(?i) his ([^ ,]*)'," "+txt_srch.group(1)+" of "+name_pre,txt)
				text[i] = txt

			t[j]['text'] = '\n'.join(text)

		for j,out_txt in enumerate(t):

			text = out_txt['text']
			text = text.split('\n')
			fut_txt = ''
			for i,txt in enumerate(text):
				words = txt.split(',')
				txt=''
				for i in words[1:]:
					txt+= words[0]+","+i+"\n"
				fut_txt+= txt

			t[j]['text'] = fut_txt
		#self.insert ('relation_text',{'text':s})

		#grammer = 'NP: {} {<JJ.?>*<NN.?>+}'
		#grammer = 'NP: {<JJ.?>* <NN.?>+}'
		grammer = r"""
  NP:
  	{<JJ.?|NN.?>+ <IN|TO>}
    {<NNP.?>+}
  """	
		co=1
  		post=dict()
  		pp =''
		for j,out_txt in enumerate(t):

			text = out_txt['text']
			text = text.split('\n')
			for i,txt in enumerate(text):
				got_chunk = self.chuncking(txt,grammer)
				name1=''
				relation=list()
				name2=''
				flag=0
				for jj in got_chunk:
					jj=str(jj)
					jj = jj.split(' ')
					jj = jj[1:]
					if flag==0 and len(jj)==1:
						name1 += jj[0][:jj[0].find('/')]+" "
						pass
						continue
					else:
						flag=1

					if flag==1 and len(jj)==2:
						relation.append(jj[0][:jj[0].find('/')].lower().strip())
						pass
						continue
					else:
						flag=2

					if flag==2 and len(jj)==1:
						name2 += jj[0][:jj[0].find('/')]+" "
				if name1 == '' or name2 =='' or len(relation)==0:
					continue
				post[co]=dict()
				post[co]['name1'] = name1.lower().strip()
				post[co]['name2'] = name2.lower().strip()
				post[co]['relation'] = relation
				post[co]['play'] = t[j]['name']
				co+=1
				pp+=name1+"||"+name2+"||"+','.join(relation)+"||"+t[j]['name']+"\n"
		#return post
		#txt = '\n'.join(['='*32+i['name']+'='*32+"\n"+i['text'] for i in t])
		#text = self.tagging(txt)
		file('relation.txt','w').write(pp)
		#print text
		pass
	pass

def main():
	x=extraction("http://www.gutenberg.org/cache/epub/100/pg100.txt")
	y=database('chinmaydb')
	z=word_featuring(x,y)
	

	#---------------------completed task-------------------
	#x.extract()
	#x.export_file('shakesphere.txt')
	#x.import_file('shakesphere.txt')
	#y.store_files(x.create_text(False))      #first task complete

	#y.store_names(z.names())                 #storing of the name in the db by the collection name == naam

	#y.store_place(z.place())				  #storing of the place in the db by the collection place == plaace
	
	#y.store_relationship(z.relationship())   #storing all the  relationship  in the db by the collection relation == relationship
	#------------------------------------------------------
	'''
	
	print y.get_place_plays("france")

	---output---
	{u'_id': 101, u'plays': [u'THE THIRD PART OF KING HENRY THE SIXTH', u'THE TRAGEDY OF KING LEAR', u'THE COMEDY OF ERRORS', u'KING HENRY THE EIGHTH', u'CYMBELINE', u'ALLS WELL THAT ENDS WELL', u'KING RICHARD THE SECOND', u'THE FIRST PART OF HENRY THE SIXTH', u'THE MERCHANT OF VENICE', u'SECOND PART OF KING HENRY IV', u"LOVE'S LABOUR'S LOST", u'KING JOHN', u'AS YOU LIKE IT', u'THE TRAGEDY OF HAMLET, PRINCE OF DENMARK', u'KING RICHARD III', u'THE FIRST PART OF KING HENRY THE FOURTH', u'THE LIFE OF KING HENRY THE FIFTH']}


	print "===================================================================="//second second task

	print y.get_name_plays("macbeth")

	---output--
	{u'_id': 532, u'plays': [u'THE TRAGEDY OF MACBETH']}

	print "===================================================================="//third second task


	print y.get_relationship("antonio","bassanio")
	[{u'play': u'THE MERCHANT OF VENICE', u'_id': 82, u'relation': [u'friend']}]


	'''
	z=y.get_all_doc('naam',{},{'name':1})
	txt = '\n'.join([i['name'] for i in z])
	file('name.txt','w').write(txt)
	#x.import_file('1.txt')
	#x.text=x.text.decode('utf-8','ignore')

	

	#file('2.txt','w').write('\n'.join(text))


	pass

main()